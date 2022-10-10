# -*- coding: utf-8 -*-

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    Message,
    WebAppInfo,
    LabeledPrice,
    ShippingOption,
    ShippingQuery,
    PreCheckoutQuery,
    successful_payment
)
from config import PAYMENTS_PROVIDER_TOKEN

my_router = Router()


@my_router.message(Command(commands=["start"]))
async def command_start(message: Message, bot: Bot, base_url: str):
    await bot.set_chat_menu_button(
        chat_id=message.chat.id,
        menu_button=MenuButtonWebApp(text="Меню", web_app=WebAppInfo(url=f"{base_url}/demo")),
    )
    await message.answer("""Ку!\nОтправь любое сообщения для начала.\nИли отправь /webview, /buy""")


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




prices = [
    LabeledPrice(label='Working Time Machine', amount=5750),
    LabeledPrice(label='Gift wrapping', amount=500),
]

# Setup shipping options
shipping_options = [
    ShippingOption(id='instant', title='WorldWide Teleporter').add(LabeledPrice(label='Teleporter', amount=1000)),
    ShippingOption(id='pickup', title='Local pickup').add(LabeledPrice(label='Pickup', amount=300)),
]


@my_router.message(commands=['buy'])
async def cmd_buy(message: Message, bot: Bot):
    await bot.send_message(message.chat.id,
                           "Real cards won't work with me, no money will be debited from your account."
                           " Use this test card number to pay for your Time Machine: `4242 4242 4242 4242`"
                           "\n\nThis is your demo invoice:", parse_mode='Markdown')
    await bot.send_invoice(message.chat.id, title='Working Time Machine',
                           description='Want to visit your great-great-great-grandparents?'
                                       ' Make a fortune at the races?'
                                       ' Shake hands with Hammurabi and take a stroll in the Hanging Gardens?'
                                       ' Order our Working Time Machine today!',
                           provider_token=PAYMENTS_PROVIDER_TOKEN,
                           currency='usd',
                           photo_url='https://telegra.ph/file/d08ff863531f10bf2ea4b.jpg',
                           photo_height=512,  # !=0/None or picture won't be shown
                           photo_width=512,
                           photo_size=512,
                           is_flexible=True,  # True If you need to set up Shipping Fee
                           prices=prices,
                           start_parameter='time-machine-example',
                           payload='HAPPY FRIDAYS COUPON')


@my_router.shipping_query(lambda query: True)
async def shipping(shipping_query: ShippingQuery, bot: Bot):
    await bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
                                    error_message='Oh, seems like our Dog couriers are having a lunch right now.'
                                                  ' Try again later!')


@my_router.pre_checkout_query(lambda query: True)
async def checkout(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Aliens tried to steal your card's CVV,"
                                                      " but we successfully protected your credentials,"
                                                      " try to pay again in a few minutes, we need a small rest.")


@my_router.message(content_types=successful_payment)
async def got_payment(message: Message, bot: Bot):
    await bot.send_message(message.chat.id,
                           'Hoooooray! Thanks for payment! We will proceed your order for `{} {}`'
                           ' as fast as possible! Stay in touch.'
                           '\n\nUse /buy again to get a Time Machine for your friend!'.format(
                               message.successful_payment.total_amount / 100, message.successful_payment.currency),
                           parse_mode='Markdown')