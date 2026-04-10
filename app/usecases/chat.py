from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.core.errors import ExternalServiceError


class ChatUseCase:
    def __init__(self, chat_repo: ChatMessageRepository, llm_client: OpenRouterClient):
        self._chat_repo = chat_repo
        self._llm_client = llm_client

    async def ask(self, user_id: int, prompt: str, system: str | None, max_history: int, temperature: float) -> str:
        # собираем историю
        history = await self._chat_repo.get_last_messages(user_id, limit=max_history)

        # формируем messages для LLM
        messages = []
        if system:
            messages.append({"role": "system", "content": system})

        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": prompt})

        # сохранить вопрос пользователя
        await self._chat_repo.add_message(user_id, "user", prompt)

        # вызов llm
        try:
            answer = await self._llm_client.chat_completion(messages, temperature)
        except ExternalServiceError:
            raise

        # сохранить ответ ассистента
        await self._chat_repo.add_message(user_id, "assistant", answer)

        return answer

    async def get_history(self, user_id: int, limit: int = 50):
        return await self._chat_repo.get_last_messages(user_id, limit)

    async def delete_history(self, user_id: int):
        await self._chat_repo.delete_history(user_id)
