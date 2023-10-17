from datetime import datetime

from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

def _is_weekend():
    return datetime.utcnow().weekday() in (5,6)


class WeekendMessageMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        if not _is_weekend():
            return await handler(event, data)


class WeekendCallbackMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]) -> Any:
        # Если сегодня не суббота и не воскресенье,
        # то продолжаем обработку.
        if not _is_weekend():
            return await handler(event, data)
        # В противном случае отвечаем на колбэк самостоятельно
        # и прекращаем дальнейшую обработку
        await event.answer(
            "Бот по выходным не работает!",
            show_alert=True)
        return