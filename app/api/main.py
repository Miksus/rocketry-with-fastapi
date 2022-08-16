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



app = FastAPI(
    title="Rocketry with FastAPI",
    description="This is a REST API for a scheduler. It uses FastAPI as the web framework and Rocketry for scheduling."
)



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




# Add routers
# -----------

app.include_router(router_config)
app.include_router(router_params)
app.include_router(router_session)
app.include_router(router_task)
app.include_router(router_logs)