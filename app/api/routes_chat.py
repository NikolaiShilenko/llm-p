from fastapi import APIRouter, Depends, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.usecases.chat import ChatUseCase
from app.api.deps import get_chat_usecase, get_current_user_id
from app.core.errors import ExternalServiceError

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    chat_uc: ChatUseCase = Depends(get_chat_usecase),
):
    try:
        answer = await chat_uc.ask(
            user_id=user_id,
            prompt=request.prompt,
            system=request.system,
            max_history=request.max_history,
            temperature=request.temperature,
        )
        return ChatResponse(answer=answer)
    except ExternalServiceError as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/history")
async def get_history(
    user_id: int = Depends(get_current_user_id),
    chat_uc: ChatUseCase = Depends(get_chat_usecase),
):
    history = await chat_uc.get_history(user_id)
    return [
        {
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "created_at": msg.created_at.isoformat()
        }
        for msg in history
    ]


@router.delete("/history")
async def delete_history(
    user_id: int = Depends(get_current_user_id),
    chat_uc: ChatUseCase = Depends(get_chat_usecase),
):
    await chat_uc.delete_history(user_id)
    return {"message": "История удалена"}
