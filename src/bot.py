from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from database.sqliter import Database
import config
import asyncio
from handlers import registration, base, services
from aiogram import types

_DEFAULT_COMMAND = [types.bot_command.BotCommand(command="start", description="Начало"),
                    types.bot_command.BotCommand(command="register", description="Регистрация"),
                    types.bot_command.BotCommand(command="service", description="Услуги"),
                    types.bot_command.BotCommand(command="help", description="Помошник"),
                    types.bot_command.BotCommand(command="cancel", description="Отмена")
                    ]


async def main() -> None:
    # main func
    db = Database(config)
    dp = Dispatcher()
    config.logger.info("* Main start *")

    bot = Bot(config.API_KEY, parse_mode=ParseMode.HTML)
    await bot.set_my_commands(_DEFAULT_COMMAND)
    dp.include_router(registration.router)
    dp.include_router(base.router)
    dp.include_router(services.router)
    await dp.start_polling(bot, db=db)


if __name__ == '__main__':
    # main loop asyncio
    asyncio.run(main())
