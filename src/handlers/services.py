import tool
from config import logger
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.register import get_reg_bt
from keyboards.service_keyboard import get_inet_bt, get_category_bt, get_photo_bt, get_archive_bt
from filters.chat_type import ChatTypeFilter
from handlers.handler_tool import CategoryCallbackFactory, send_problem
from smax.smax_api import get_status_smax, send_message_smax


router = Router()
router.message.filter(ChatTypeFilter(chat_type=["group", "supergroup"]))

# dictionary classification smax platform
_step_status = ("Класификация", "Выполнение", "Подтверждение", "Готов")
_classification_status = {"Log": _step_status[0], "Classify": _step_status[0], "FirstLineSupport": _step_status[1],
                        "Escalate": _step_status[1], "Accept": _step_status[2], "Review": _step_status[2],
                        "Close": _step_status[3], "Abandon": _step_status[3]}


class UserOrder(StatesGroup):
    """
    Personal data
    """
    name = State()
    category = State()
    subcategory = State()
    problem = State()
    cabinet = State()
    phone = State()
    photo = State()
    category_id = State()


@router.message(Command("service"))
@router.message(F.text.startswith("Новый"))
async def cmd_dice_in_group(message: Message, db):
    if not await tool.exist_user(str(message.from_user.id), db):
        await message.answer(f"Для использования данного <b>меню</b> (<em>Сервис</em>) 💬 "
                             f"необходима регистрация 🟢\n",
                             reply_markup=get_reg_bt())
        return True
    await message.answer(f"Здравствуйте 🗿, для выбора услуги выбирите соответствующую <u>кнопку</u> 🔘",
                         reply_markup=get_category_bt(db))


@router.callback_query(CategoryCallbackFactory.filter())
async def callbacks_num_change_fab(callback: CallbackQuery, callback_data: CategoryCallbackFactory,
                                   db, state: FSMContext, bot, categories):
    await bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=None)
    if callback_data.action == "change":
        await callback.answer()
        await state.update_data(name=callback_data.name)
        await state.update_data(category_id=callback_data.value_id)
        categories.append(callback_data.name)
        await state.update_data(subcategory=categories)

        sub_cat = await tool.cat_child(callback_data.value_id, db)
        if sub_cat:
            await callback.message.answer(text="Выбирете подкатегорию 👇", reply_markup=get_inet_bt(sub_cat))
        else:
            await state.set_state(UserOrder.problem)
            for idx in range(len(categories)):
                res = (idx+1) * "🔹"
                res += categories[idx]
                categories[idx] = res
            await callback.message.answer(f"\n".join(categories))
            await callback.message.answer("Опишите проблему 📝:")


@router.callback_query(UserOrder.category)
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
    await callback.message.answer(f"Вы выбрали категорию:\n🔹 <b>{data['name']}</b>\n🔹🔹 <b>{category[1]}</b>\n\n"
                                  f"Опишите проблему 📝:")


@router.message(UserOrder.problem)
async def order_msg(message: Message, state: FSMContext) -> None:
    """
    Select cabinet
    """
    await state.update_data(problem=message.text)
    await state.set_state(UserOrder.cabinet)
    await message.answer(text="Укажите <u>номер</u> <em>кабинет</em> 🚪")


@router.message(UserOrder.cabinet)
async def order_msg(message: Message, state: FSMContext) -> None:
    """
    Select cabinet
    """
    await state.update_data(cabinet=message.text)
    await state.set_state(UserOrder.phone)
    await message.answer(text="Укажите <u>номер</u> <em>телефона</em> ☎")


@router.message(UserOrder.phone)
async def order_msg(message: Message, state: FSMContext) -> None:
    """
    Register user
    """
    await state.update_data(phone=message.text)
    await state.set_state(UserOrder.photo)
    await message.answer(text="Загрузите одно <u>фото</u> описываемой проблемы 📸", reply_markup=get_photo_bt())


@router.callback_query(UserOrder.photo, F.data.startswith("photo_"))
async def category_sub(callback: CallbackQuery, state: FSMContext, bot, db, categories) -> None:
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
    await state.clear()
    order_id = await send_message_smax(data, person)
    await tool.set_order(data, person[0], order_id, db)
    # await send_problem(data, person)
    categories.clear()
    logger.info(f"User by email {person[2]} created order without photo")
    await callback.message.answer(text=f"Ваше обращение оптравленно без фото. Спасибо Ваш № заявки {order_id} в обработке ⚙")


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
        await message.answer(text="Ваше обращение отправленно с фото. Спасибо Ваша заявка в обработке ⚙")
        logger.info(f"User by email {person[2]} created order with photo")


@router.message(Command("orders"))
async def get_all_orders(message: Message, db, user_uuid=None, active=False):
    """
    View all records by user
    """
    if user_uuid:
        my_orders = await tool.get_orders(str(user_uuid), active, db)
    else:
        my_orders = await tool.get_orders(str(message.from_user.id), active, db)
    if not my_orders:
        if not active:
            await message.answer(text="У Вас нет активных заявок! ⭕")
        else:
            await message.answer(text="Архив пуст! ⭕")
        return
    for item in my_orders:
        res = await get_status_smax(item[2])
        current_status = res["entities"][0]["properties"]["PhaseId"]
        query_time = res["meta"]["query_time"]
        await tool.update_status_order(item, _classification_status[current_status], db, query_time)

        await message.answer(text=f"Дата создания: 🕗 {item[1].strftime('%Y-%m-%d %H:%M')}\n"
                                  f"Ваш номер заявки: 🆔 {item[2]}\n"
                                  f"Ваш статус заявки: 🔰 {_classification_status[current_status]}\n"
                                  f"Тема: ❕ <em>{item[5]}</em>\n"
                                  f"Текст обращения: 💬 {item[4]}\n")
    if not active:
        await message.answer(text="<em>Просмотреть архив заявок 🗂</em>", reply_markup=get_archive_bt())


@router.callback_query(F.data.startswith("archive_"))
async def category_sub(callback: CallbackQuery, db, bot) -> None:
    """
    Archive orders
    """
    await bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=None)

    await callback.answer()
    await get_all_orders(callback.message, db, user_uuid=callback.from_user.id, active=True)
