import logging
from fastapi.routing import APIRouter

from src.api.user_handlers import user_router
from src.api.marks_handlers import marks_router

from fastapi import FastAPI

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="EL_Api")

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(marks_router, prefix="/marks", tags=["marks"])

app.include_router(main_api_router)
