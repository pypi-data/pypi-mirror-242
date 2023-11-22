import asyncio
import json

from ChatGPT2API.V1 import AsyncChatbot
from ChatGPT2API.V1 import Chatbot

config = json.load(open("/home/peanut996/.config/ChatGPT2API/config.json"))


async def main() -> None:
    chatbot = AsyncChatbot(config)
    async for message in chatbot.ask("Hello, how are you?"):
        print(message.get("message"))

    print(await chatbot.share_conversation())


def sync_main():
    chatbot = Chatbot(config)
    for message in chatbot.ask("Hello, how are you?"):
        print(message.get("message"))


asyncio.run(main())
