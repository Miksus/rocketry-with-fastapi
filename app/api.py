"""
This file contains FastAPI app.
Modify the routes as you wish.
"""

import datetime
import time
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, validator
from redbird.oper import in_, between, greater_equal

from fastapi import APIRouter, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from scheduler import app as app_rocketry

app = FastAPI(
    title="Rocketry with FastAPI",
    description="This is a REST API for a scheduler. It uses FastAPI as the web framework and Rocketry for scheduling."
)
session = app_rocketry.session


# Enable CORS so that the React application 
# can communicate with FastAPI. Modify these
# if you put it to production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models (for serializing JSON)
# -----------------------------

class Task(BaseModel):
    name: str
    description: Optional[str]
    priority: int

    start_cond: str
    end_cond: str
    timeout: Optional[int]

    disabled: bool
    force_termination: bool
    force_run: bool

    status: str
    is_running: bool
    last_run: Optional[datetime.datetime]
    last_success: Optional[datetime.datetime]
    last_fail: Optional[datetime.datetime]
    last_terminate: Optional[datetime.datetime]
    last_inaction: Optional[datetime.datetime]
    last_crash: Optional[datetime.datetime]

class Log(BaseModel):
    timestamp: Optional[datetime.datetime] = Field(alias="created")
    task_name: str
    action: str

# Session Config
# --------------

router_config = APIRouter(tags=["config"])

@router_config.get("/session/config")
async def get_session_config():
    return session.config

@router_config.patch("/session/config")
async def patch_session_config(values:dict):
    for key, val in values.items():
        setattr(session.config, key, val)


# Session Parameters
# ------------------

router_params = APIRouter(tags=["session parameters"])

@router_params.get("/session/parameters")
async def get_session_parameters():
    return session.parameters

@router_params.get("/session/parameters/{name}")
async def get_session_parameters(name):
    return session.parameters[name]

@router_params.put("/session/parameters/{name}")
async def put_session_parameter(name:str, value):
    session.parameters[name] = value

@router_params.delete("/session/parameters/{name}")
async def delete_session_parameter(name:str):
    del session.parameters[name]


# Session Actions
# ---------------

router_session = APIRouter(tags=["session"])

@router_session.post("/session/shut_down")
async def shut_down_session():
    session.shut_down()


# Task
# ----

router_task = APIRouter(tags=["task"])

@router_task.get("/tasks", response_model=List[Task])
async def get_tasks():
    return [
        Task(
            start_cond=str(task.start_cond), 
            end_cond=str(task.end_cond),
            is_running=task.is_running,
            **task.dict(exclude={'start_cond', 'end_cond'})
        )
        for task in session.tasks
    ]

@router_task.get("/tasks/{task_name}")
async def get_task(task_name:str):
    return session[task_name]
    
@router_task.patch("/tasks/{task_name}")
async def patch_task(task_name:str, values:dict):
    task = session[task_name]
    for attr, val in values.items():
        setattr(task, attr, val)


# Task Actions
# ------------

@router_task.post("/tasks/{task_name}/disable")
async def disable_task(task_name:str):
    task = session[task_name]
    task.disabled = True

@router_task.post("/tasks/{task_name}/enable")
async def enable_task(task_name:str):
    task = session[task_name]
    task.disabled = False

@router_task.post("/tasks/{task_name}/terminate")
async def disable_task(task_name:str):
    task = session[task_name]
    task.force_termination = True

@router_task.post("/tasks/{task_name}/run")
async def run_task(task_name:str):
    task = session[task_name]
    task.force_run = True


# Logging
# -------

router_logs = APIRouter(tags=["logs"])

@router_logs.get("/logs", description="Get tasks")
async def get_task_logs(action: Optional[List[Literal['run', 'success', 'fail', 'terminate', 'crash', 'inaction']]] = Query(default=[]),
                        min_created: Optional[int]=Query(default=None), max_created: Optional[int] = Query(default=None),
                        past: Optional[int]=Query(default=None),
                        limit: Optional[int]=Query(default=None),
                        task: Optional[List[str]] = Query(default=None)):
    filter = {}
    if action:
        filter['action'] = in_(action)
    if (min_created or max_created) and not past:
        filter['created'] = between(min_created, max_created, none_as_open=True)
    elif past:
        filter['created'] = greater_equal(time.time() - past)
    
    if task:
        filter['task_name'] = in_(task)

    repo = session.get_repo()
    logs = repo.filter_by(**filter).all()
    if limit:
        logs = logs[max(len(logs)-limit, 0):]
    logs = sorted(logs, key=lambda log: log.created, reverse=True)
    logs = [Log(**vars(log)) for log in logs]

    return logs

@router_logs.get("/task/{task_name}/logs", description="Get tasks")
async def get_task_logs(task_name:str,
                        action: Optional[List[Literal['run', 'success', 'fail', 'terminate', 'crash', 'inaction']]] = Query(default=[]),
                        min_created: Optional[int]=Query(default=None), max_created: Optional[int] = Query(default=None)):
    filter = {}
    if action:
        filter['action'] = in_(action)
    if min_created or max_created:
        filter['created'] = between(min_created, max_created, none_as_open=True)

    return session[task_name].logger.filter_by(**filter).all()


# Add routers
# -----------

app.include_router(router_config)
app.include_router(router_params)
app.include_router(router_session)
app.include_router(router_task)
app.include_router(router_logs)