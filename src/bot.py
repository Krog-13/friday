from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.enums.menu_button_type import MenuButtonType
from database.sqliter import Database
from aiohttp.web import run_app
from aiohttp.web_app import Application
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
import config
import datetime
from handlers import registration, base, services, sing_ecp
from aiogram import types
from handlers.sing_ecp import get_file_sign
from aiohttp.web_fileresponse import FileResponse
from aiohttp.web_request import Request


# start server https -> ngrok http 8080
APP_BASE_URL = config.APP_BASE_URL

# set emoji ctrl+alt+;
_DEFAULT_COMMAND = [types.bot_command.BotCommand(command="start", description="Домашняя страница 🟢"),
                    types.bot_command.BotCommand(command="register", description="Регистрация 🔵"),
                    types.bot_command.BotCommand(command="service", description="Услуги 🌀"),
                    types.bot_command.BotCommand(command="file", description="Файл 📄"),
                    types.bot_command.BotCommand(command="orders", description="Ваши заявки 📒"),
                    types.bot_command.BotCommand(command="help", description="Помошник 💡"),
                    types.bot_command.BotCommand(command="cancel", description="Отмена 👾")]

_DEFAULT_COMMAND_TYPE = MenuButtonType.COMMANDS
_categories = []

async def on_startup(bot: Bot, base_url: str):
    await bot.set_webhook(f"{base_url}/webhook")
    await bot.send_message(chat_id="838019137", text=f"Bot started at {datetime.datetime.now().strftime('%Y.%m.%d %H:%M')}")
    await bot.set_my_commands(_DEFAULT_COMMAND)
    # await bot.set_chat_menu_button(
    #     menu_button=MenuButtonWebApp(text="Open Menu", web_app=WebAppInfo(url=f"{base_url}/demo")))


async def demo_handler(request: Request):
    return FileResponse("demo.html")


def main() -> None:
    # main func
    db = Database(config)
    config.logger.info("* Main start *")
    bot = Bot(config.API_KEY, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp["base_url"] = APP_BASE_URL
    dp.startup.register(on_startup)

    dp.include_router(registration.router)
    dp.include_router(base.router)
    dp.include_router(services.router)
    dp.include_router(sing_ecp.router)

    app = Application()
    app["bot"] = bot

    app.router.add_get("/mgovSign", get_file_sign)
    app.router.add_get("/demo", demo_handler)
    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        db=db,
        categories=_categories
    ).register(app, path="/webhook")

    setup_application(app, dp, bot=bot, db=db, category=_categories)
    run_app(app, host="127.0.0.1", port=8080)


if __name__ == '__main__':
    # main loop asyncio
    config.logger.info("Entry point")
    main()
