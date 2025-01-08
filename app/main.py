import os

from fastapi import FastAPI

from app import routers

app = FastAPI(
    debug=True if os.environ.get("DEBUG") else False,
    title="Shop Docs"
)

auth = FastAPI(
    debug=True if os.environ.get("DEBUG") else False,
    title="Shop Auth",
)

auth.include_router(routers.groups.router)
auth.include_router(routers.permissions.router)
auth.include_router(routers.users.router)

app.mount("/auth", auth)
