from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.for_questions import get_yes_no_kb

router = Router()

@router.message(Command("one"))
async def cmd_start(message: Message):
    await message.answer(
        "Are you enjoi your job?",
        reply_markup=get_yes_no_kb())

@router.message(F.text.lower() == "yes")
async def answer_yes(message: Message):
    await message.answer(
        "this is cool",
        reply_markup=ReplyKeyboardRemove())

@router.message(F.text.lower() == "no")
async def answer_yes(message: Message):
    await message.answer(
        "yeap I understand you!",
        reply_markup=ReplyKeyboardRemove())