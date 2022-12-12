
import asyncio

from rocketry import Grouper
from rocketry.conds import every
from rocketry.args import Task, Return, Session

group = Grouper()

# Put your tasks here

@group.task(every('10 seconds', based="finish"))
async def do_permanently():
    "This runs for really long time"
    await asyncio.sleep(60)

@group.task(every('2 seconds', based="finish"))
async def do_short():
    "This runs for short time"
    await asyncio.sleep(1)

@group.task(every('20 seconds', based="finish"))
async def do_long():
    "This runs for long time"
    await asyncio.sleep(60)

@group.task(every('10 seconds', based="finish"))
async def do_fail():
    "This fails constantly"
    await asyncio.sleep(10)
    raise RuntimeError("Whoops!")