from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.repositories.users import UserRepository
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase
from app.core.security import decode_access_token
from app.core.errors import UnauthorizedError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


async def get_chat_repo(db: AsyncSession = Depends(get_db)) -> ChatMessageRepository:
    return ChatMessageRepository(db)


async def get_llm_client() -> OpenRouterClient:
    return OpenRouterClient()


async def get_auth_usecase(user_repo: UserRepository = Depends(get_user_repo)) -> AuthUseCase:
    return AuthUseCase(user_repo)


async def get_chat_usecase(
    chat_repo: ChatMessageRepository = Depends(get_chat_repo),
    llm_client: OpenRouterClient = Depends(get_llm_client),
) -> ChatUseCase:
    return ChatUseCase(chat_repo, llm_client)


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
        return user_id
    except UnauthorizedError as e:
        raise HTTPException(status_code=401, detail=str(e))
