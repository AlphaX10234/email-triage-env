"""
inference.py — Baseline inference script for Email Triage OpenEnv.
"""
import os
import json
import sys
import time
import requests
import subprocess

# Force correct httpx version at runtime
subprocess.run(
    [sys.executable, "-m", "pip", "install",
     "httpx==0.27.2", "openai==1.54.0", "-q", "--force-reinstall"],
    check=True
)

# ── Configuration ─────────────────────────────────────────────────────────────
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api-inference.huggingface.co/v1")
MODEL_NAME   = os.environ.get("MODEL_NAME",   "meta-llama/Llama-3.1-8B-Instruct")
HF_TOKEN     = os.environ.get("HF_TOKEN",     "")
ENV_BASE_URL = os.environ.get("ENV_BASE_URL", "http://localhost:7860")

TASKS = ["task_1_easy", "task_2_medium", "task_3_hard"]

client = None  # set in main()

SYSTEM_PROMPT = """You are an expert email triage assistant. Your job is to:
1. Read each email carefully
2. Assign it the correct PRIORITY: urgent, high, normal, low, or spam
3. Assign the correct CATEGORY: customer_complaint, billing, technical_support, general_inquiry, spam, internal, sales, or legal
4. Choose the best ACTION: reply, forward, archive, delete, escalate, or flag
5. Optionally specify assign_to (who to route it to)
6. Optionally write a brief reply_draft if action is "reply"
7. Always explain your reason briefly
You MUST respond with valid JSON only, in this exact format:
{
  "priority": "urgent|high|normal|low|spam",
  "category": "customer_complaint|billing|technical_support|general_inquiry|spam|internal|sales|legal",
  "action": "reply|forward|archive|delete|escalate|flag",
  "assign_to": "team_name or null",
  "reply_draft": "draft text or null",
  "reason": "brief explanation"
}"""

FALLBACK_ACTION = {
    "priority":    "normal",
    "category":    "general_inquiry",
    "action":      "archive",
    "assign_to":   None,
    "reply_draft": None,
    "reason":      "Fallback due to LLM error",
}


def call_llm(email_obs: dict) -> dict:
    email = email_obs["email"]
    user_message = f"""Please triage this email:
Subject: {email['subject']}
From: {email['sender']}
Received: {email['received_at']}
Has Attachment: {email['has_attachment']}
Thread Length: {email['thread_length']}
Body:
{email['body']}
Context: {email_obs.get('context', '')}
Respond with JSON only."""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message},
        ],
        temperature=0.0,
        max_tokens=500,
    )

    content = response.choices[0].message.content.strip()
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    content = content.strip()
    return json.loads(content)


def run_task(task_id: str) -> dict:
    print(f"\n{'='*60}")
    print(f"  Task: {task_id}")
    print(f"{'='*60}")

    try:
        reset_resp = requests.post(
            f"{ENV_BASE_URL}/reset",
            json={"task_id": task_id, "session_id": task_id},
            timeout=30,
        )
        reset_resp.raise_for_status()
    except Exception as e:
        print(f"  [ERROR] Could not reset task {task_id}: {e}", file=sys.stderr)
        raise

    data = reset_resp.json()
    obs  = data["observation"]

    # ── Structured output: task start ─────────────────────────────────────────
    print(f"[START] task={task_id}", flush=True)

    step_scores = []
    step_num    = 0

    while True:
        step_num += 1
        email_subject = obs["email"]["subject"]
        display = email_subject[:50] + "..." if len(email_subject) > 50 else email_subject
        print(f"\n  Step {step_num} | Email: '{display}'")

        try:
            action = call_llm(obs)
        except Exception as e:
            print(f"    LLM error: {e}. Using fallback action.", file=sys.stderr)
            action = FALLBACK_ACTION.copy()

        print(f"    -> priority={action.get('priority')} | "
              f"category={action.get('category')} | action={action.get('action')}")

        try:
            step_resp = requests.post(
                f"{ENV_BASE_URL}/step",
                json={"action": action, "session_id": task_id},
                timeout=30,
            )
            step_resp.raise_for_status()
        except Exception as e:
            print(f"  [ERROR] Step request failed: {e}", file=sys.stderr)
            raise

        step_data = step_resp.json()
        reward    = step_data.get("reward", {})
        done      = step_data.get("done", False)
        info      = step_data.get("info", {})

        score    = reward.get("score", 0.0)
        feedback = reward.get("feedback", "")
        print(f"    Score: {score:.3f} | {str(feedback)[:80]}")
        step_scores.append(score)

        # ── Structured output: step ───────────────────────────────────────────
        print(f"[STEP] step={step_num} reward={score:.4f}", flush=True)

        if done:
            avg               = sum(step_scores) / len(step_scores) if step_scores else 0.0
            passing_threshold = info.get("passing_threshold", 0.5)
            passed            = avg >= passing_threshold
            print(f"\n  Task complete! Avg score: {avg:.4f} | "
                  f"{'PASSED' if passed else 'FAILED'}")

            # ── Structured output: task end ───────────────────────────────────
            print(f"[END] task={task_id} score={avg:.4f} steps={step_num}", flush=True)

            return {
                "task_id":           task_id,
                "step_scores":       step_scores,
                "avg_score":         round(avg, 4),
                "passed":            passed,
                "passing_threshold": passing_threshold,
            }

        obs = step_data.get("observation", obs)
        time.sleep(0.5)


def main():
    global client

    print("\n" + "="*60)
    print("  Email Triage OpenEnv — Baseline Inference Script")
    print(f"  Model: {MODEL_NAME}")
    print(f"  API:   {API_BASE_URL}")
    print("="*60)

    if not HF_TOKEN:
        print("\n[ERROR] HF_TOKEN environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    if not MODEL_NAME:
        print("\n[ERROR] MODEL_NAME environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=HF_TOKEN,
            base_url=API_BASE_URL,
        )
        print("\n✓ OpenAI client initialised")
    except Exception as e:
        print(f"\n[ERROR] Failed to initialise OpenAI client: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        health = requests.get(f"{ENV_BASE_URL}/health", timeout=10)
        health.raise_for_status()
        print(f"✓ Environment healthy at {ENV_BASE_URL}")
    except Exception as e:
        print(f"\n[ERROR] Cannot reach environment at {ENV_BASE_URL}: {e}", file=sys.stderr)
        sys.exit(1)

    results = []
    for task_id in TASKS:
        try:
            result = run_task(task_id)
        except Exception as e:
            print(f"\n[ERROR] Task {task_id} failed with exception: {e}", file=sys.stderr)
            sys.exit(1)
        results.append(result)

    print("\n" + "="*60)
    print("  FINAL RESULTS SUMMARY")
    print("="*60)
    overall_scores = []
    for r in results:
        status = "PASSED" if r["passed"] else "FAILED"
        print(f"  {r['task_id']:25s} | Score: {r['avg_score']:.4f} | {status}")
        overall_scores.append(r["avg_score"])

    overall_avg = sum(overall_scores) / len(overall_scores) if overall_scores else 0.0
    print(f"\n  Overall average score: {overall_avg:.4f}")
    print("="*60)

    output = {
        "model":        MODEL_NAME,
        "api_base_url": API_BASE_URL,
        "results":      results,
        "overall_avg":  round(overall_avg, 4),
    }
    with open("baseline_results.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\n  Results saved to baseline_results.json")


if __name__ == "__main__":
    main()
