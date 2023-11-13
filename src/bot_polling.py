from aiogram.enums.menu_button_type import MenuButtonType
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher
from aiogram import types
from handlers import registration, base, services, sing_ecp
from database.sqliter import Database
import datetime
import config
import asyncio


# start server https -> ngrok http 8080
APP_BASE_URL = config.APP_BASE_URL
_DEFAULT_COMMAND_TYPE = MenuButtonType.COMMANDS
_categories = []

# set emoji ctrl+alt+;
_DEFAULT_COMMAND = [types.bot_command.BotCommand(command="start", description="Домашняя страница 🟢"),
                    types.bot_command.BotCommand(command="register", description="Регистрация 🔵"),
                    types.bot_command.BotCommand(command="service", description="Услуги 🌀"),
                    # types.bot_command.BotCommand(command="file", description="Файл 📄"),
                    types.bot_command.BotCommand(command="orders", description="Мои заявки 📒"),
                    types.bot_command.BotCommand(command="help", description="Помошник 💡"),
                    types.bot_command.BotCommand(command="cancel", description="Отмена 👾")]


async def on_startup(bot: Bot):
    await bot.send_message(chat_id="838019137", text=f"Bot started at {datetime.datetime.now().strftime('%Y.%m.%d %H:%M')}")
    await bot.set_my_commands(_DEFAULT_COMMAND)


async def main() -> None:
    # main func
    db = Database(config)
    config.logger.info("* Main start *")
    bot = Bot(config.API_KEY, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.startup.register(on_startup)

    dp.include_router(registration.router)
    dp.include_router(base.router)
    dp.include_router(services.router)
    dp.include_router(sing_ecp.router)

    await dp.start_polling(bot, db=db, categories=_categories)

if __name__ == '__main__':
    # main loop asyncio
    config.logger.info("Entry point")
    asyncio.run(main())
