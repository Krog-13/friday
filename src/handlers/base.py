from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Router
from filters.chat_type import ChatTypeFilter


router = Router()
router.message.filter(ChatTypeFilter(chat_type=["group", "supergroup"]))


@router.message(CommandStart())
async def cmd_dice_in_group(message: Message):
        await message.answer(f"Здравствуйте Вас привествует смарт-бот 'КазМунайГаз' Какая-то информация \n\nДля дальнейшего пользования необходимо "
                             f"зарегистрироваться. Используйте меню для навигации\n")
