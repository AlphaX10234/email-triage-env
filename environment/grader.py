"""
Graders for each task. Each grader returns a score between 0.0 and 1.0.
Graders are deterministic and reproducible.
"""
from typing import Dict, Any, Tuple


PRIORITY_ADJACENCY = {
    # Maps (predicted, actual) -> partial credit
    ("urgent", "high"): 0.6,
    ("high", "urgent"): 0.6,
    ("high", "normal"): 0.4,
    ("normal", "high"): 0.4,
    ("normal", "low"): 0.4,
    ("low", "normal"): 0.4,
    ("spam", "low"): 0.2,
    ("low", "spam"): 0.2,
}

ACTION_CATEGORY_COMPATIBILITY = {
    # Valid action choices for each category
    "customer_complaint": ["reply", "escalate", "flag"],
    "billing": ["forward", "escalate", "reply"],
    "technical_support": ["forward", "escalate", "reply"],
    "general_inquiry": ["reply", "forward", "archive"],
    "spam": ["delete", "archive"],
    "internal": ["archive", "reply", "forward"],
    "sales": ["forward", "reply"],
    "legal": ["escalate", "forward", "flag"],
}


def grade_priority(predicted: str, actual: str) -> Tuple[float, bool]:
    """Returns (score, is_exact_match)."""
    if predicted == actual:
        return 1.0, True
    partial = PRIORITY_ADJACENCY.get((predicted, actual), 0.0)
    return partial, False


def grade_category(predicted: str, actual: str) -> Tuple[float, bool]:
    """Returns (score, is_exact_match)."""
    if predicted == actual:
        return 1.0, True
    # Partial credit for spam misclassification (less severe)
    if actual == "spam" and predicted in ["general_inquiry", "internal"]:
        return 0.3, False
    return 0.0, False


def grade_action(action: str, category: str, priority: str) -> Tuple[float, bool]:
    """Returns (score, is_appropriate)."""
    valid_actions = ACTION_CATEGORY_COMPATIBILITY.get(category, [])
    if action in valid_actions:
        return 1.0, True
    # Partial credit if action is "flag" for urgent items
    if priority == "urgent" and action == "flag":
        return 0.5, False
    # Partial credit if action is "archive" for low priority
    if priority in ["low", "spam"] and action == "archive":
        return 0.6, False
    return 0.0, False


def compute_step_reward(
    action_dict: Dict[str, Any],
    ground_truth: Dict[str, Any],
    task_difficulty: str,
) -> Dict[str, Any]:
    """
    Compute the reward for a single step.
    Returns a dict with all reward components.
    """
    pred_priority = action_dict.get("priority", "")
    pred_category = action_dict.get("category", "")
    pred_action = action_dict.get("action", "")

    gt_priority = ground_truth["priority"]
    gt_category = ground_truth["category"]
    gt_action = ground_truth["action"]

    # Grade each component
    priority_score, priority_exact = grade_priority(pred_priority, gt_priority)
    category_score, category_exact = grade_category(pred_category, gt_category)
    action_score, action_appropriate = grade_action(pred_action, gt_category, gt_priority)

    # Weights vary by component
    # Priority: 35%, Category: 35%, Action: 30%
    weighted_score = (priority_score * 0.35) + (category_score * 0.35) + (action_score * 0.30)

    # Bonus: if all three are correct, small bonus
    if priority_exact and category_exact and action_appropriate:
        weighted_score = min(1.0, weighted_score + 0.05)

    # Penalty: if spam is completely missed (security concern)
    if gt_priority == "spam" and pred_priority != "spam" and pred_action != "delete":
        weighted_score = max(0.0, weighted_score - 0.1)

    # Penalty: if urgent is misclassified as low or spam
    if gt_priority == "urgent" and pred_priority in ["low", "spam"]:
        weighted_score = max(0.0, weighted_score - 0.2)

    # Build feedback string
    feedback_parts = []
    if priority_exact:
        feedback_parts.append(f"✓ Priority '{pred_priority}' correct.")
    else:
        feedback_parts.append(f"✗ Priority: predicted '{pred_priority}', expected '{gt_priority}' (score: {priority_score:.2f}).")
    
    if category_exact:
        feedback_parts.append(f"✓ Category '{pred_category}' correct.")
    else:
        feedback_parts.append(f"✗ Category: predicted '{pred_category}', expected '{gt_category}' (score: {category_score:.2f}).")

    if action_appropriate:
        feedback_parts.append(f"✓ Action '{pred_action}' appropriate.")
    else:
        feedback_parts.append(f"✗ Action: '{pred_action}' not ideal for category '{gt_category}' (score: {action_score:.2f}).")

    return {
        "score": round(weighted_score, 4),
        "priority_correct": priority_exact,
        "category_correct": category_exact,
        "action_appropriate": action_appropriate,
        "partial_credit": round(weighted_score, 4),
        "feedback": " ".join(feedback_parts),
    }
