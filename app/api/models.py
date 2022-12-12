import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional

class TaskModel(BaseModel):
    name: str
    description: Optional[str]
    priority: int

    start_cond: str
    end_cond: str
    timeout: Optional[int]

    permanent: bool
    multilaunch: Optional[bool]
    disabled: bool

    force_termination: bool
    force_run: bool

    status: Optional[str]
    is_running: bool
    set_running: bool
    last_run: Optional[datetime.datetime]
    last_success: Optional[datetime.datetime]
    last_fail: Optional[datetime.datetime]
    last_terminate: Optional[datetime.datetime]
    last_inaction: Optional[datetime.datetime]
    last_crash: Optional[datetime.datetime]

    batches: list

    @validator("start_cond", pre=True)
    def parse_start_cond(cls, value):
        return str(value)

    @validator("end_cond", pre=True)
    def parse_end_cond(cls, value):
        return str(value)

    @classmethod
    def from_task(cls, task):
        extra_attrs = (
            "status",
            "last_run", "last_success", "last_fail", "last_terminate", "last_crash", "last_inaction",
            "is_running"
        )
        attrs = task.dict()
        attrs.update(
            {
                attr: getattr(task, attr)
                for attr in extra_attrs
            }
            
        )
        attrs["set_running"] = task.batches != []
        return cls(**attrs)

class Log(BaseModel):
    timestamp: Optional[datetime.datetime] = Field(alias="created")
    task_name: str
    action: str