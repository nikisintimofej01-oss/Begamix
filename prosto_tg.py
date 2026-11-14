# prosto-tg: Простая библиотека для Telegram
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

class ProstoTG:
    def __init__(self, token):
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.handlers = {}

    def create_cmd(self, command):
        """Декоратор для создания команды"""
        def decorator(func):
            self.handlers[command] = func
            return func
        return decorator

    async def run(self):
        # Регистрируем все команды
        for cmd, func in self.handlers.items():
            self.dp.message.register(func, Command(cmd.replace("/", "")))
        
        print(f"[prosto-tg] Bot started with {len(self.handlers)} commands!")
        await self.dp.start_polling(self.bot)
