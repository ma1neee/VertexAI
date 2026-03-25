# test_api.py
import asyncio
import sys

sys.path.insert(0, 'src')

from src.core.agent import agent
from src.models.settings import app_settings


async def test():
    agent.set_config(app_settings.qwen_api_key, app_settings.qwen_api_url)

    response = await agent.request(
        chat_id="test-chat",
        message="Ответь одним словом: готов?",
        system="Ты тестовый ассистент."
    )

    print("✅ Ответ от API:", response)


asyncio.run(test())