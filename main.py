# -*- coding: utf-8 -*-

import coloredlogs
import logging

from aiohttp.web import run_app
from aiohttp.web_app import Application
from handlers import my_router
from routes import check_data_handler, demo_handler, send_message_handler

from aiogram import Bot, Dispatcher
from aiogram.types import MenuButtonWebApp, WebAppInfo, BotCommand, BotCommandScopeChat
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config import API_TOKEN, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_URL, LOG_LEVEL, LOG_STYLE, LOG_FORMAT, PARSE_MODE


async def on_startup(bot: Bot, base_url: str):
    await bot.set_webhook(f"{base_url}/webhook")
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="Меню", web_app=WebAppInfo(url=f"{base_url}/demo"))
    )


async def set_bot_commands(bot: Bot, chat_id: int):
    commands = [BotCommand(command='start', description='Главное меню'),]
                #BotCommand(command='report', description='Сообщение разработчику')]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeChat(chat_id=chat_id))


def main():
    logger = logging.getLogger(name=__name__)
    coloredlogs.install(level=LOG_LEVEL, level_styles=LOG_STYLE, fmt=LOG_FORMAT)

    bot = Bot(token=API_TOKEN, parse_mode=PARSE_MODE)
    dispatcher = Dispatcher()
    dispatcher["base_url"] = WEBHOOK_URL
    dispatcher.startup.register(on_startup)
    dispatcher.include_router(my_router)

    app = Application()
    app["bot"] = bot

    app.router.add_get("/demo", demo_handler)
    app.router.add_post("/demo/checkData", check_data_handler)
    app.router.add_post("/demo/sendMessage", send_message_handler)
    SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
    ).register(app, path="/webhook")
    setup_application(app, dispatcher, bot=bot)

    logger.debug(msg='Starting bot')
    run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logging.error(msg='Bot stopped!')
