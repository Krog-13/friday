from aiogram import Bot, Dispatcher
from aiogram.types import MenuButtonWebApp, WebAppInfo
from aiogram.enums import ParseMode
from database.sqliter import Database
from aiohttp.web import run_app
from aiohttp import web
from aiohttp.web_app import Application
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
import config
import asyncio
from pathlib import Path
from aiohttp.web_fileresponse import FileResponse
from aiohttp.web_request import Request
from handlers import registration, base, services, sing_ecp
from aiogram import types
from handlers.sing_ecp import get_file_sign

# start server https -> ngrok http 8080
APP_BASE_URL = "https://ebb8-92-46-127-106.ngrok.io"

_DEFAULT_COMMAND = [types.bot_command.BotCommand(command="start", description="Начало"),
                    types.bot_command.BotCommand(command="register", description="Регистрация"),
                    types.bot_command.BotCommand(command="service", description="Услуги"),
                    types.bot_command.BotCommand(command="file", description="Файл"),
                    types.bot_command.BotCommand(command="help", description="Помошник"),
                    types.bot_command.BotCommand(command="cancel", description="Отмена")]


async def on_startup(bot: Bot, base_url: str):
    await bot.set_webhook(f"{base_url}/webhook")
    await bot.send_message(chat_id="838019137", text="Bot has been started")


async def demo_handler(request: Request):
    query = request.query["file_path"]
    return web.Response(text="<h1>Test request</h1>", content_type="text/html")


def main() -> None:
    # main func
    db = Database(config)
    config.logger.info("* Main start *")
    bot = Bot(config.API_KEY, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp["base_url"] = APP_BASE_URL
    dp.startup.register(on_startup)

    # bot.set_my_commands(_DEFAULT_COMMAND)
    dp.include_router(registration.router)
    dp.include_router(base.router)
    dp.include_router(services.router)
    dp.include_router(sing_ecp.router)

    app = Application()
    app["bot"] = bot

    app.router.add_get("/mgovSign", get_file_sign)
    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        db=db
    ).register(app, path="/webhook")
        
    setup_application(app, dp, bot=bot, db=db)
    run_app(app, host="127.0.0.1", port=8080)


if __name__ == '__main__':
    # main loop asyncio
    config.logger.info("Entry point")
    main()
    # asyncio.run(main())
