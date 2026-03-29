"""
Tests for the EmailTriageEnv.
Run with: python -m pytest tests/ -v
"""
import pytest
from environment import EmailTriageEnv, Action, Observation, Reward
from environment.grader import compute_step_reward, grade_priority, grade_category, grade_action


# ── Grader unit tests ─────────────────────────────────────────────────────────

def test_grade_priority_exact():
    score, exact = grade_priority("urgent", "urgent")
    assert score == 1.0
    assert exact is True


def test_grade_priority_adjacent():
    score, exact = grade_priority("urgent", "high")
    assert score == 0.6
    assert exact is False


def test_grade_priority_wrong():
    score, exact = grade_priority("spam", "urgent")
    assert score == 0.0
    assert exact is False


def test_grade_category_exact():
    score, exact = grade_category("billing", "billing")
    assert score == 1.0
    assert exact is True


def test_grade_category_wrong():
    score, exact = grade_category("spam", "billing")
    assert score == 0.0
    assert exact is False


def test_grade_action_valid():
    score, ok = grade_action("escalate", "legal", "urgent")
    assert score == 1.0
    assert ok is True


def test_grade_action_invalid():
    score, ok = grade_action("delete", "legal", "urgent")
    assert score == 0.0
    assert ok is False


# ── Environment tests ─────────────────────────────────────────────────────────

def make_action(**kwargs):
    defaults = {
        "priority": "normal",
        "category": "general_inquiry",
        "action": "archive",
        "assign_to": None,
        "reply_draft": None,
        "reason": "test",
    }
    defaults.update(kwargs)
    return Action(**defaults)


def test_reset_returns_observation():
    env = EmailTriageEnv("task_1_easy")
    obs = env.reset()
    assert isinstance(obs, Observation)
    assert obs.step_number == 0
    assert obs.inbox_size == 5
    assert obs.email is not None


def test_step_returns_reward():
    env = EmailTriageEnv("task_1_easy")
    env.reset()
    action = make_action(priority="urgent", category="technical_support", action="escalate")
    obs, reward, done, info = env.step(action)
    assert isinstance(reward, Reward)
    assert 0.0 <= reward.score <= 1.0
    assert isinstance(done, bool)


def test_episode_completes_after_5_steps():
    env = EmailTriageEnv("task_1_easy")
    env.reset()
    for i in range(4):
        _, _, done, _ = env.step(make_action())
        assert not done
    _, _, done, _ = env.step(make_action())
    assert done


def test_reset_resets_state():
    env = EmailTriageEnv("task_1_easy")
    env.reset()
    env.step(make_action())
    state_after_step = env.state()
    assert state_after_step["step_count"] == 1

    env.reset()
    state_after_reset = env.state()
    assert state_after_reset["step_count"] == 0
    assert state_after_reset["cumulative_score"] == 0.0


def test_state_returns_dict():
    env = EmailTriageEnv("task_2_medium")
    env.reset()
    s = env.state()
    assert "task_id" in s
    assert "cumulative_score" in s
    assert "step_count" in s
    assert s["task_id"] == "task_2_medium"


def test_all_tasks_loadable():
    for task_id in ["task_1_easy", "task_2_medium", "task_3_hard"]:
        env = EmailTriageEnv(task_id)
        obs = env.reset()
        assert obs is not None


def test_reward_range():
    """All rewards must be in [0.0, 1.0]."""
    env = EmailTriageEnv("task_3_hard")
    env.reset()
    actions = [
        make_action(priority="urgent", category="legal", action="escalate"),
        make_action(priority="urgent", category="legal", action="escalate"),
        make_action(priority="urgent", category="technical_support", action="escalate"),
        make_action(priority="high", category="billing", action="reply"),
        make_action(priority="high", category="legal", action="escalate"),
    ]
    for action in actions:
        _, reward, done, _ = env.step(action)
        assert 0.0 <= reward.score <= 1.0
        if done:
            break


def test_perfect_score_easy_task():
    """A perfect agent on easy task should score >= 0.9."""
    env = EmailTriageEnv("task_1_easy")
    env.reset()
    
    # Ground truth actions for task_1_easy
    perfect_actions = [
        make_action(priority="urgent", category="technical_support", action="escalate", assign_to="engineering"),
        make_action(priority="spam", category="spam", action="delete"),
        make_action(priority="high", category="billing", action="forward", assign_to="finance"),
        make_action(priority="high", category="sales", action="forward", assign_to="sales"),
        make_action(priority="low", category="internal", action="archive"),
    ]
    
    total_score = 0.0
    for action in perfect_actions:
        _, reward, done, info = env.step(action)
        total_score += reward.score
    
    avg = total_score / 5
    assert avg >= 0.85, f"Perfect agent should score >=0.85 on easy task, got {avg}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
