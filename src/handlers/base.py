from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram import Router
from filters.chat_type import ChatTypeFilter
from aiogram.fsm.context import FSMContext

router = Router()
router.message.filter(ChatTypeFilter(chat_type=["group", "supergroup"]))


@router.message(CommandStart())
async def cmd_dice_in_group(message: Message):
        await message.answer(f"Здравствуйте Вас привествует смарт-бот 'КазМунайГаз' Какая-то информация \n\nДля дальнейшего пользования необходимо "
                             f"зарегистрироваться. Используйте меню для навигации\n")


@router.message(Command("help"))
async def helper(message: Message):
        await message.answer(f"Здравствуйте Вас привествует смарт-бот 'КазМунайГаз'\nПри возникновений вопросов по пользованию бота прошу написать на почту - <b>a.nurkin@kmg.kz</b>")


@router.message(Command("cancel"))
async def canceled_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Сброс")
