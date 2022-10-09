from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    Message,
    WebAppInfo,
)

my_router = Router()


@my_router.message(Command(commands=["start"]))
async def command_start(message: Message, bot: Bot, base_url: str):
    await bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=MenuButtonWebApp(text="Меню", web_app=WebAppInfo(url=f"{base_url}/demo")),
    )
    await message.answer("""Ку!\nОтправь любое сообщения для начала.\nИли отправь /webview""")


@my_router.message(Command(commands=["webview"]))
async def command_webview(message: Message, base_url: str):
    await message.answer(
        "Отлично! Теперь ты можешь попробовать отправить его через Webview",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Открыть Webview", web_app=WebAppInfo(url=f"{base_url}/demo")
                    )
                ]
            ]
        ),
    )


@my_router.message(~F.message.via_bot)  # Echo to all messages except messages via bot
async def echo_all(message: Message, base_url: str):
    await message.answer(
        "Тест Webview",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Открыть", web_app=WebAppInfo(url=f"{base_url}/demo"))]
            ]
        ),
    )
