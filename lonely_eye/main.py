from fastapi import FastAPI

from lonely_eye.config import settings
from lonely_eye.cameras.router import router as cameras_router
from lonely_eye.cars_owners.router import router as car_owners_router
from lonely_eye.violations.router import router as violations_router
from lonely_eye.workers.router import router as workers_router
from lonely_eye.managers.router import router as managers_router

app = FastAPI(
    title=settings.api_title,
    root_path=settings.api_prefix,
)

app.include_router(
    router=cameras_router,
    prefix="/cameras",
    tags=["Cameras"],
)

app.include_router(
    router=car_owners_router,
    prefix="/cars_owners",
    tags=["Cars Owners"],
)

app.include_router(
    router=violations_router,
    prefix="/violations",
    tags=["Violations"],
)

app.include_router(
    router=workers_router,
    prefix="/workers",
    tags=["Workers"],
)

app.include_router(
    router=managers_router,
    prefix="/managers",
    tags=["Managers"],
)
#  TODO: Реализовать базовую схему для отправки ответов
#  TODO: Создать отдельные файлы для кастомных ошибок
