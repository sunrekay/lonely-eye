import uvicorn
from fastapi import FastAPI

from config import settings
from cameras.router import router as cameras_router

app = FastAPI(title=settings.api_title)

app.include_router(
    router=cameras_router,
    prefix=settings.api_prefix,
)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
