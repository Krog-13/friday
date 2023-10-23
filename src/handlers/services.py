import tool
from config import logger
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.register import get_reg_bt
from keyboards.service_keyboard import get_inet_bt, get_category_bt, get_photo_bt
from filters.chat_type import ChatTypeFilter
from handlers.handler_tool import CategoryCallbackFactory, send_problem


router = Router()
router.message.filter(ChatTypeFilter(chat_type=["group", "supergroup"]))


class UserOrder(StatesGroup):
    """
    Personal data
    """
    name = State()
    category = State()
    subcategory = State()
    problem = State()
    photo = State()
    category_id = State()


@router.message(Command("service"))
async def cmd_dice_in_group(message: Message, db):
    if not await tool.exist_user(str(message.from_user.id), db):
        await message.answer(f"Для использования данного <b>меню</b> (<em>Сервис</em>) "
                             f"необходима регистрация\n",
                             reply_markup=get_reg_bt())
        return True
    await message.answer(f"Здравствуйте, для выбора услуги выбирите соответствующую кнопку",
                         reply_markup=get_category_bt(db))


@router.callback_query(CategoryCallbackFactory.filter())
async def callbacks_num_change_fab(callback: CallbackQuery, callback_data: CategoryCallbackFactory,
                                   db, state: FSMContext, bot):
    # Текущее значение
    await bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=None)
    if callback_data.action == "change":
        await callback.answer()
        await state.update_data(name=callback_data.name)
        sub_cat = await tool.cat_child(callback_data.value_id, db)
        await state.set_state(UserOrder.category)
        await callback.message.answer(text="Выбирете подкатегорию", reply_markup=get_inet_bt(sub_cat, callback_data.name))


@router.callback_query(UserOrder.category, F.data.startswith("fix_"))
async def category_sub(callback: CallbackQuery, state: FSMContext, bot) -> None:
    """
    """
    await bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=None)
    category = callback.data.split("_")
    await state.update_data(subcategory=category[1])
    await state.update_data(category_id=category[2])
    await state.set_state(UserOrder.problem)
    data = await state.get_data()
    await callback.answer()
    await callback.message.answer(f"Вы выбрали категорию:\n* <b>{data['name']}</b>\n** <b>{category[1]}</b>\n\n"
                                  f"Опишите проблему:")


@router.message(UserOrder.problem)
async def order_msg(message: Message, state: FSMContext) -> None:
    """
    Register user
    """
    await state.update_data(problem=message.text)
    await state.set_state(UserOrder.photo)
    await message.answer(text="Загрузите фото описываемой проблемы", reply_markup=get_photo_bt())


@router.callback_query(UserOrder.photo, F.data.startswith("photo_"))
async def category_sub(callback: CallbackQuery, state: FSMContext, bot, db) -> None:
    """
    Without photo
    """
    await bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=None)
    await callback.answer()
    uuid = callback.from_user.id
    person = await tool.get_user(str(uuid), db)
    data = await state.get_data()
    await tool.set_order(data, person[0], db)
    await state.clear()
    await send_problem(data, person)
    logger.info(f"User by email {person[2]} created order without photo")
    await callback.message.answer(text="Ваше обращение оптравленно без фото. Спасибо Ваша заявка в обработке")


@router.message(UserOrder.photo, F.photo)
async def order_photo(message: Message, state: FSMContext, db, bot) -> None:
    """
    With photo
    """
    uuid = message.from_user.id
    person = await tool.get_user(str(uuid), db)
    data = await state.get_data()
    await state.clear()
    await bot.download(message.photo[-1], destination=f"/tmp/{message.photo[-1].file_id}.jpg")
    file = await bot.get_file(message.photo[-1].file_id)
    file_path = file.file_path
    photo_bytes = await bot.download_file(file_path)
    if data:
        await tool.set_order(data, person[0], db)
        await send_problem(data, person, photo_bytes)
        await message.answer(text="Ваше обращение отправленно с фото. Спасибо Ваша заявка в обработке")
        logger.info(f"User by email {person[2]} created order with photo")


@router.message(Command("orders"))
async def get_all_orders(message: Message, db):
    """
    View all records by user
    """
    my_orders = await tool.get_orders(str(message.from_user.id), db)
    if not my_orders:
        await message.answer(text="У Вас нет активных заявок!")
        return
    for item in my_orders:
        await message.answer(text=f"Дата создания: {item[0].strftime('%Y-%m-%d %H:%M')}\n"
                                  f"Статус: {item[1]}\n"
                                  f"Тема: {item[3]}\n"
                                  f"Текст обращения: {item[2]}\n")
