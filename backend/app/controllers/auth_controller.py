from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.models import User
from app.schemas.schemas import UserRegister, UserLogin, Token, UserResponse
from app.auth.security import hash_password, verify_password, create_access_token

class AuthController:
    @staticmethod
    async def register(db: AsyncSession, payload: UserRegister) -> Token:
        # Check existing user
        result = await db.execute(select(User).where(User.email == payload.email))
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email address is already registered."
            )

        hashed_pwd = hash_password(payload.password)
        new_user = User(
            name=payload.name,
            email=payload.email,
            password_hash=hashed_pwd,
            role="user"
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        access_token = create_access_token(data={"sub": new_user.id, "email": new_user.email})
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.model_validate(new_user)
        )

    @staticmethod
    async def login(db: AsyncSession, payload: UserLogin) -> Token:
        result = await db.execute(select(User).where(User.email == payload.email))
        user = result.scalars().first()
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email credentials or password."
            )

        access_token = create_access_token(data={"sub": user.id, "email": user.email})
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.model_validate(user)
        )

auth_controller = AuthController()
