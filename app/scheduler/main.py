"""
This file contains Rocketry app.
Add your tasks here, conditions etc. here.
"""
from redbird.repos import SQLRepo, MemoryRepo
from sqlalchemy import create_engine

from rocketry import Rocketry
from rocketry.args import TaskLogger, Config, EnvArg
from rocketry.log import MinimalRecord

app = Rocketry(config={"execution": "async"})

from .tasks import example

@app.setup()
def setup_app(logger=TaskLogger(), config=Config(), env=EnvArg("ENV", default="dev")):
    "Set up the app"
    if env == "prod":
        conn_string = "sqlite:///app.db"
        repo = SQLRepo(engine=create_engine(conn_string), table="tasks", model=MinimalRecord, id_field="created", if_missing="create")

        config.silence_task_prerun = True
        config.silence_task_logging = True
        config.silence_cond_check = True
    else:
        repo = MemoryRepo(model=MinimalRecord, if_missing="create")

        config.silence_task_prerun = False
        config.silence_task_logging = False
        config.silence_cond_check = False
    
    logger.set_repo(repo)

app.include_grouper(example.group)

if __name__ == "__main__":
    # Run only Rocketry
    app.run()