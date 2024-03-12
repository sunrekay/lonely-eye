from fastapi import FastAPI

from lonely_eye.config import settings
from lonely_eye.cameras.router import router as cameras_router
from lonely_eye.cars_owners.router import router as car_owners_router

app = FastAPI(title=settings.api_title)

app.include_router(
    router=cameras_router,
    prefix=settings.api_prefix,
)
app.include_router(
    router=car_owners_router,
    prefix=settings.api_prefix,
)
