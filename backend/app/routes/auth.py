from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.schemas.schemas import UserRegister, UserLogin, Token, UserResponse
from app.controllers.auth_controller import auth_controller
from app.auth.security import get_current_user
from app.models.models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, status_code=201)
async def register(payload: UserRegister, db: AsyncSession = Depends(get_db)):
    return await auth_controller.register(db, payload)

@router.post("/login", response_model=Token)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    return await auth_controller.login(db, payload)

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)
