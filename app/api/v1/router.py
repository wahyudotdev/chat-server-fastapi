from fastapi import APIRouter
from .endpoints.auth.handler import router as auth_router
from .endpoints.user.handler import router as user_router
from .endpoints.home.handler import router as home_router
from .endpoints.chat.handler import router as chat_router

router = APIRouter()

router.include_router(auth_router, prefix='/auth', tags=['Auth'])
router.include_router(user_router, prefix='/user', tags=['User'])
router.include_router(home_router, prefix="/home", tags=["Home"])
router.include_router(chat_router, prefix="/chat", tags=["Chat"])