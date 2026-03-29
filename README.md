# 📧 Email Triage OpenEnv

A real-world **email triage environment** for training and evaluating AI agents on enterprise inbox management tasks.

Built for the **OpenEnv Hackathon (Round 1)** — fully compliant with the OpenEnv specification.

---

## 🌍 Environment Description

**Email triage** is a task every professional does daily: reading incoming emails and deciding what to do with them — prioritize, categorize, reply, forward, escalate, or discard. It requires:

- Natural language understanding
- Business context awareness  
- Risk assessment (legal, security, billing)
- Appropriate routing and escalation decisions

This environment simulates a realistic enterprise inbox where an agent must process a sequence of emails, making correct triage decisions under time pressure.

---

## 🎯 Tasks

| Task ID | Name | Difficulty | Emails | Passing Threshold |
|---------|------|------------|--------|-------------------|
| `task_1_easy` | Basic Email Triage | Easy | 5 | 0.70 |
| `task_2_medium` | Nuanced Email Routing | Medium | 5 | 0.60 |
| `task_3_hard` | Complex & Ambiguous Triage | Hard | 5 | 0.50 |

### Task 1 — Easy
Clear, unambiguous emails: production outage alerts, obvious spam, overdue invoices, sales inquiries, and internal announcements. Signals are explicit; a capable agent should score above 0.85.

### Task 2 — Medium  
Emails that require reading comprehension: repeated complaints (thread history matters), API technical issues with a sales angle, contract renewals, GDPR data requests, and bug reports. Requires nuanced judgment about urgency and routing.

### Task 3 — Hard  
High-stakes, ambiguous emails: partnership pitches with implicit urgency, legal demand letters, responsible security disclosures, vulnerable customers with billing confusion, and complex multi-part GDPR requests. Frontier models score ~0.55–0.65. Weak models fail.

---

## 📐 Observation Space

Each observation is a JSON object:

```json
{
  "email": {
    "id": "t1_001",
    "subject": "URGENT: Server down - production outage",
    "sender": "ops-alerts@company.com",
    "body": "Our main production server...",
    "received_at": "2024-03-15T14:15:00Z",
    "has_attachment": false,
    "thread_length": 1
  },
  "inbox_size": 5,
  "step_number": 0,
  "max_steps": 5,
  "previous_action": null,
  "task_id": "task_1_easy",
  "context": "Task: Basic Email Triage (easy difficulty)..."
}
```

---

## 🎮 Action Space

Each action is a JSON object:

```json
{
  "priority": "urgent",
  "category": "technical_support",
  "action": "escalate",
  "assign_to": "engineering",
  "reply_draft": null,
  "reason": "Production outage requires immediate engineering response."
}
```

**Priority options:** `urgent` | `high` | `normal` | `low` | `spam`

**Category options:** `customer_complaint` | `billing` | `technical_support` | `general_inquiry` | `spam` | `internal` | `sales` | `legal`

**Action options:** `reply` | `forward` | `archive` | `delete` | `escalate` | `flag`

---

## 🏆 Reward Function

The reward is **dense** (every step gives a signal) and ranges from **0.0 to 1.0**.

| Component | Weight | Scoring |
|-----------|--------|---------|
| Priority | 35% | 1.0 for exact, partial credit for adjacent (e.g. urgent↔high = 0.6) |
| Category | 35% | 1.0 for exact match only |
| Action | 30% | 1.0 if action is compatible with the correct category |

**Bonuses:**
- `+0.05` if all three components are correct (perfect triage)

**Penalties:**
- `-0.10` for missing spam (letting spam through)
- `-0.20` for classifying `urgent` as `low` or `spam` (dangerous downgrade)

---

## 🚀 Setup & Usage

### Option 1: Docker (recommended)

```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/email-triage-env
cd email-triage-env

docker build -t email-triage-env .
docker run -p 7860:7860 email-triage-env
```

### Option 2: Local Python

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 7860
```

### Run baseline inference

```bash
export API_BASE_URL=https://api.openai.com/v1
export MODEL_NAME=gpt-4o-mini
export HF_TOKEN=your_openai_api_key
export ENV_BASE_URL=http://localhost:7860

python inference.py
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Environment info |
| `GET` | `/health` | Health check (returns `{"status": "ok"}`) |
| `POST` | `/reset` | Reset environment, returns first observation |
| `POST` | `/step` | Take action, returns (obs, reward, done, info) |
| `GET` | `/state` | Full environment state |
| `GET` | `/tasks` | List all tasks |

### Example: Reset

```bash
curl -X POST http://localhost:7860/reset \
  -H "Content-Type: application/json" \
  -d '{"task_id": "task_1_easy", "session_id": "my_session"}'
```

### Example: Step

```bash
curl -X POST http://localhost:7860/step \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "my_session",
    "action": {
      "priority": "urgent",
      "category": "technical_support",
      "action": "escalate",
      "assign_to": "engineering",
      "reason": "Production outage"
    }
  }'
```

---

## 📊 Baseline Scores

Measured with `gpt-4o-mini` (temperature=0):

| Task | Score | Status |
|------|-------|--------|
| task_1_easy | ~0.89 | ✅ PASSED |
| task_2_medium | ~0.72 | ✅ PASSED |
| task_3_hard | ~0.58 | ✅ PASSED |
| **Overall** | **~0.73** | ✅ |

---

## 📁 Project Structure

```
email-triage-env/
├── app.py                    # FastAPI server (OpenEnv HTTP interface)
├── inference.py              # Baseline inference script
├── openenv.yaml              # OpenEnv metadata
├── Dockerfile                # Container definition
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── environment/
    ├── __init__.py
    ├── env.py                # EmailTriageEnv (step/reset/state)
    ├── models.py             # Pydantic models (Observation, Action, Reward)
    ├── grader.py             # Deterministic graders for each task
    └── data.py               # Email dataset (15 emails across 3 tasks)
```

---

## 📜 OpenEnv Compliance

- ✅ Typed `Observation`, `Action`, `Reward` Pydantic models
- ✅ `step(action)` → returns `(observation, reward, done, info)`
- ✅ `reset()` → returns initial observation
- ✅ `state()` → returns full environment state
- ✅ `openenv.yaml` with complete metadata
- ✅ 3 tasks with difficulty progression (easy → medium → hard)
- ✅ Graders produce scores in `[0.0, 1.0]` range
- ✅ Dense reward function (not sparse)
- ✅ Baseline `inference.py` using OpenAI client
- ✅ Dockerfile + HuggingFace Spaces deployment

---

## 👤 Author

Hussanpreet Soni — OpenEnv Hackathon 2024
