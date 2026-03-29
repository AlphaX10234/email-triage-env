"""
FastAPI application exposing the EmailTriageEnv via HTTP.
Implements the OpenEnv standard endpoints.
"""
import os
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from environment import EmailTriageEnv, Action

app = FastAPI(
    title="Email Triage OpenEnv",
    description="A real-world email triage environment for training and evaluating AI agents.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store environments per session
_envs: Dict[str, EmailTriageEnv] = {}


def _get_env(session_id: str) -> EmailTriageEnv:
    if session_id not in _envs:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found. Call /reset first.")
    return _envs[session_id]


class ResetRequest(BaseModel):
    task_id: Optional[str] = "task_1_easy"
    session_id: Optional[str] = "default"


class StepRequest(BaseModel):
    action: Dict[str, Any]
    session_id: Optional[str] = "default"


@app.get("/")
def root():
    return {
        "name": "Email Triage OpenEnv",
        "version": "1.0.0",
        "tasks": ["task_1_easy", "task_2_medium", "task_3_hard"],
        "endpoints": ["/reset", "/step", "/state", "/health"],
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/reset")
def reset(req: ResetRequest):
    """Reset the environment and return the first observation."""
    env = EmailTriageEnv(task_id=req.task_id)
    _envs[req.session_id] = env
    obs = env.reset()
    return {
        "observation": obs.model_dump(),
        "session_id": req.session_id,
        "task_id": req.task_id,
    }


@app.post("/step")
def step(req: StepRequest):
    """Take an action and return (observation, reward, done, info)."""
    env = _get_env(req.session_id)
    try:
        action = Action(**req.action)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid action: {e}")

    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.model_dump(),
        "reward": reward.model_dump(),
        "done": done,
        "info": info,
    }


@app.get("/state")
def state(session_id: str = "default"):
    """Return the full current state of the environment."""
    env = _get_env(session_id)
    return env.state()


@app.get("/tasks")
def list_tasks():
    """List all available tasks with descriptions."""
    from environment.data import ALL_TASKS
    return {
        task_id: {
            "name": cfg["name"],
            "description": cfg["description"],
            "difficulty": cfg["difficulty"],
            "num_emails": len(cfg["emails"]),
            "passing_threshold": cfg["passing_threshold"],
        }
        for task_id, cfg in ALL_TASKS.items()
    }
