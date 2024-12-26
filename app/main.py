from fastapi import FastAPI

from app.users.routers.auth_router import router as router_auth
from app.users.routers.user_router import router as router_current_user
from app.users.routers.manager_router import router as router_manager
from app.users.routers.sub_router import router as router_sub
app = FastAPI()

app.include_router(router_auth)
app.include_router(router_current_user)
app.include_router(router_manager)
app.include_router(router_sub)