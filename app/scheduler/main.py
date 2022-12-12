"""
This file contains Rocketry app.
Add your tasks here, conditions etc. here.
"""
from redbird.repos import SQLRepo
from sqlalchemy import create_engine

from rocketry import Rocketry
from rocketry.args import TaskLogger, Config, EnvArg
from rocketry.log import MinimalRecord

from .tasks import example

app = Rocketry(config={"execution": "async"})

@app.setup()
def setup_app(logger=TaskLogger(), config=Config(), env=EnvArg("ENV", default="dev")):
    "Set up the app"
    repo = SQLRepo(engine=create_engine("sqlite:///app.db"), table="tasks", model=MinimalRecord, id_field="created")
    logger.set_repo(repo)
    if env == "prod":
        config.silence_task_prerun = True
        config.silence_task_logging = True
        config.silence_cond_check = True
    else:
        config.silence_task_prerun = False
        config.silence_task_logging = False
        config.silence_cond_check = False

app.include_grouper(example.group)

if __name__ == "__main__":
    # Run only Rocketry
    app.run()