"""
This file contains Rocketry app.
Add your tasks here, conditions etc. here.
"""
import asyncio
from rocketry import Rocketry
from rocketry.conds import every

app = Rocketry(config={"task_execution": "async"})

@app.task(every('10 seconds', based="finish"))
async def do_permanently():
    "This runs for really long time"
    await asyncio.sleep(600000)

@app.task(every('2 seconds', based="finish"))
async def do_short():
    "This runs for short time"
    await asyncio.sleep(1)

@app.task(every('20 seconds', based="finish"))
async def do_long():
    "This runs for long time"
    await asyncio.sleep(60)

@app.task(every('10 seconds', based="finish"))
async def do_fail():
    "This fails constantly"
    await asyncio.sleep(10)
    raise RuntimeError("Whoops!")

if __name__ == "__main__":
    # Run only Rocketry
    app.run()