from fastapi import FastAPI
from fastapi.routing import APIRouter

from api.user_handlers import user_router
from api.marks_handlers import marks_router

# create instance of the app
app = FastAPI(title="EL_Api")


# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(marks_router, prefix="/marks", tags=["marks"])

app.include_router(main_api_router)
