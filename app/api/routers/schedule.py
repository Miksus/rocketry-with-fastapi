from typing import List, Optional, Literal
import time

from fastapi import APIRouter, Query
from redbird.oper import between, in_, greater_equal

from app.scheduler.main import app as app_rocketry
from app.api.models import Log, TaskModel

session = app_rocketry.session


# Session Config
# --------------

router = APIRouter(tags=["Rocketry"])

@router.get("/session/config", tags=["config"])
async def get_session_config():
    return session.config.dict(exclude={"time_func", "func_run_id", "cls_lock"})

@router.patch("/session/config", tags=["config"])
async def patch_session_config(values:dict):
    for key, val in values.items():
        setattr(session.config, key, val)

# Session Parameters
# ------------------

@router.get("/session/parameters", tags=["parameters"])
async def get_session_parameters():
    return session.parameters

@router.get("/session/parameters/{name}", tags=["parameters"])
async def get_session_parameters(name):
    return session.parameters[name]

@router.put("/session/parameters/{name}", tags=["parameters"])
async def put_session_parameter(name:str, value):
    session.parameters[name] = value

@router.delete("/session/parameters/{name}", tags=["parameters"])
async def delete_session_parameter(name:str):
    del session.parameters[name]


# Session Actions
# ---------------

@router.post("/session/shut_down", tags=["session"])
async def shut_down_session():
    session.shut_down()


# Task
# ----

@router.get("/tasks", response_model=List[TaskModel], tags=["task"])
async def get_tasks():
    return [
        TaskModel.from_task(task)
        for task in session.tasks
    ]

@router.get("/tasks/{task_name}", tags=["task"])
async def get_task(task_name:str):
    return TaskModel.from_task(session[task_name])
    
@router.patch("/tasks/{task_name}", tags=["task"])
async def patch_task(task_name:str, values:dict):
    task = session[task_name]
    for attr, val in values.items():
        setattr(task, attr, val)


# Task Actions
# ------------

@router.post("/tasks/{task_name}/disable", tags=["task"])
async def disable_task(task_name:str):
    task = session[task_name]
    task.disabled = True

@router.post("/tasks/{task_name}/enable", tags=["task"])
async def enable_task(task_name:str):
    task = session[task_name]
    task.disabled = False

@router.post("/tasks/{task_name}/terminate", tags=["task"])
async def disable_task(task_name:str):
    task = session[task_name]
    task.force_termination = True

@router.post("/tasks/{task_name}/run", tags=["task"])
async def run_task(task_name:str):
    task = session[task_name]
    task.force_run = True


# Logging
# -------

@router.get("/logs", description="Get tasks", tags=["logs"])
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

@router.get("/task/{task_name}/logs", description="Get tasks", tags=["logs"])
async def get_task_logs(task_name:str,
                        action: Optional[List[Literal['run', 'success', 'fail', 'terminate', 'crash', 'inaction']]] = Query(default=[]),
                        min_created: Optional[int]=Query(default=None), max_created: Optional[int] = Query(default=None)):
    filter = {}
    if action:
        filter['action'] = in_(action)
    if min_created or max_created:
        filter['created'] = between(min_created, max_created, none_as_open=True)

    return session[task_name].logger.filter_by(**filter).all()
