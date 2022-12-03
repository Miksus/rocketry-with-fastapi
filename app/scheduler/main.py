"""
This file contains Rocketry app.
Add your tasks here, conditions etc. here.
"""
from rocketry import Rocketry
from .tasks import example

app = Rocketry(config={"task_execution": "async"})

app.include_grouper(example.group)

if __name__ == "__main__":
    # Run only Rocketry
    app.run()