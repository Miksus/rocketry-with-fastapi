"""
This file combines the two applications.
"""

import asyncio
import logging

import uvicorn

from app.api.main import app as app_fastapi
from app.scheduler.main import app as app_rocketry


class Server(uvicorn.Server):
    """Customized uvicorn.Server
    
    Uvicorn server overrides signals and we need to include
    Rocketry to the signals."""
    def handle_exit(self, sig: int, frame) -> None:
        print("Shutting", self.force_exit)
        app_rocketry.session.shut_down(force=self.force_exit)
        return super().handle_exit(sig, frame)

async def run_apps(fastapi=True, rocketry=True):
    "Run Rocketry and FastAPI"
    server = Server(config=uvicorn.Config(app_fastapi, workers=1, loop="asyncio"))

    apps = []
    if fastapi:
        task = asyncio.create_task(server.serve())
        apps.append(task)
    if rocketry:
        task = asyncio.create_task(app_rocketry.serve())
        apps.append(task)

    await asyncio.wait(apps)


def main(**kwargs):
    "Run Rocketry and FastAPI"

    # Print Rocketry's logs to terminal
    logger = logging.getLogger("rocketry.task")
    logger.addHandler(logging.StreamHandler())

    # Start the apps
    asyncio.run(run_apps(**kwargs))

if __name__ == "__main__":
    main()