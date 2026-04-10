from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError
from app.api.deps import get_auth_usecase, get_current_user_id

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic)
async def register(data: RegisterRequest, auth_uc: AuthUseCase = Depends(get_auth_usecase)):
    try:
        user = await auth_uc.register(data.email, data.password)
        return user
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), auth_uc: AuthUseCase = Depends(get_auth_usecase)):
    try:
        token = await auth_uc.login(form_data.username, form_data.password)
        return TokenResponse(access_token=token)
    except UnauthorizedError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me", response_model=UserPublic)
async def get_me(user_id: int = Depends(get_current_user_id), auth_uc: AuthUseCase = Depends(get_auth_usecase)):
    try:
        user = await auth_uc.get_profile(user_id)
        return user
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
