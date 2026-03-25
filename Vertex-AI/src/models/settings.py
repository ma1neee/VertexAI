from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os


class AppSettings(BaseSettings):
    # Явно разрешаем None + указываем дефолты из твоих ключей
    qwen_api_key: Optional[str] = Field(
        default="qw-C3489w32vWZBuW5b5gWkqcykKHlIv6m0HYSIEYHHbihRjC4Gm5LsOfs45ME1dZC8",
        alias="QWEN_API_KEY"
    )
    qwen_api_url: Optional[str] = Field(
        default="https://api.teefusion.net/qwen",
        alias="QWEN_API_URL"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        # Пробуем читать .env из нескольких мест
        env_nested_delimiter="__"
    )

    # Метод для отладки: покажет, какие значения реально загрузились
    def debug_print(self):
        print(f"🔑 qwen_api_key: {'✅ задан' if self.qwen_api_key else '❌ None'}")
        print(f"🌐 qwen_api_url: {self.qwen_api_url}")


# Создаём экземпляр
app_settings = AppSettings()

# Отладочный вывод при старте (можно убрать потом)
if __name__ == "__main__":
    app_settings.debug_print()