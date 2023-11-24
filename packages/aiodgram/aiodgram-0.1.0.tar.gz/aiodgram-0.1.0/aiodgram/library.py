from aiogram import Dispatcher, Bot, executor, types


class TgBot:

    """
    Your Telegram Bot for sent messages, photo and video
    
    
    imported in library
    :import Dispatcher
    :import Bot
    :import executor
    :import types
    :import asyncio

    All modules, without types, used for work defines in library. 
    Module types don't used in library, but you can use it instead aiogram.types .

    """

    def __init__(self,
                token: str = None):
        """
        For settings, your Telegram Bot.
        
        :param token: str, token your TG Bot, from BotFather, default None.
        """

        self.token = token
        self.bot = Bot(token)
        self.dp = Dispatcher(self.bot)
        self.executor = executor


    async def send_message(self,
                       chat_id: int,
                       message: str,
                       reply_markup = None
                       ) -> None:
        """
        For sent message from your bot.

        :param chat_id: chat ID user who used bot
        :param message: your message
        :param reply_markup: your markup for message, default None

        :return None
        """

        await self.bot.send_message(chat_id=chat_id,
                                    text=message,
                                    reply_markup=reply_markup)

    async def send_photo(self,
                         chat_id: int,
                         photo: str,
                         caption: str = None) -> None:
        """
        For sent photo from your bot.

        :param chat_id: chat id user who used bot
        :param photo: you're photoed
        :param caption: text under photo in this msg, default None

        :return None
        """

        await self.bot.send_photo(chat_id=chat_id,
                                  photo=photo,
                                  caption=caption)


    async def send_video(self,
                        chat_id: int,
                        video: str) -> None:

        """
        For send video.
        
        :param chat_id: int, chat ID user who used bot
        :param video: str, link for video

        :return None
        """
        

        await self.bot.send_video(chat_id=chat_id,
                                    video=open(f'{video}.mp4', 'rb'))


    def start_polling(self,
                      dispatcher = None,
                      skip_updates = True,
                      on_startup = None,
                      on_shutdown = None) -> None:

        """
        For start your Telegram Bot.
        
        :param dp: Dispatcher, use bot.dp, default None
        :param skip_updates: False|True, default True
        :param on_startup: your define for startup, default None
        :param on_shutdown: your define for shutdown, default None

        :return None
        """

        self.executor.start_polling(dispatcher=dispatcher,
                                    skip_updates=skip_updates,
                                    on_startup=on_startup,
                                    on_shutdown=on_shutdown)
