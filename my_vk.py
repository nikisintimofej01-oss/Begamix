# my-vk: Простая библиотека для VK
from vkbottle.bot import Bot, Message
from vkbottle import BotLabeler

class MyVK:
    def __init__(self, token):
        self.bot = Bot(token=token)
        self.labeler = BotLabeler()
        self.bot.labeler.load(self.labeler)

    def cmd(self, command):
        """Декоратор для создания команды"""
        def decorator(func):
            @self.labeler.message(text=command)
            async def wrapper(message: Message):
                await func(message)
            return func
        return decorator

    def run(self):
        print(f"[my-vk] Bot started!")
        self.bot.run_forever()
