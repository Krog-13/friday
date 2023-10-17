import tool
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from aiogram.fsm.state import State, StatesGroup
from keyboards.register import get_reg_bt
from keyboards.service_keyboard import get_inet_bt, get_category_bt
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
    category_id = State()


@router.message(Command("service"))
async def cmd_dice_in_group(message: Message, db):
    if not await tool.exist_user(str(message.from_user.id), db):
        await message.answer(f"Здравствуйте Вас привествует смарт-бот 'КазМунайГаз'"
                             f"для регистрации нажмите соответствующую кнопку\n",
                             reply_markup=get_reg_bt())
        return True
    await message.answer(f"Здравствуйте, для выбора услуги выбирите соответствующую кнопку",
                         reply_markup=get_category_bt(db))


@router.callback_query(CategoryCallbackFactory.filter())
async def callbacks_num_change_fab(callback: CallbackQuery, callback_data: CategoryCallbackFactory, db, state: FSMContext):
    # Текущее значение
    if callback_data.action == "change":
        await callback.answer()
        await state.update_data(name=callback_data.name)
        sub_cat = await tool.cat_child(callback_data.value_id, db)
        await state.set_state(UserOrder.category)
        await callback.message.answer(text="Выбирете подкатегорию", reply_markup=get_inet_bt(sub_cat, callback_data.name))


@router.callback_query(UserOrder.category, F.data.startswith("fix_"))
async def checkin_lang(callback: CallbackQuery, state: FSMContext) -> None:
    """
    """
    category = callback.data.split("_")
    await state.update_data(subcategory=category[1])
    await state.update_data(category_id=category[2])
    await state.set_state(UserOrder.problem)
    data = await state.get_data()
    await callback.answer()
    await callback.message.answer(f"Вы выбрали категорию:\n<b>{data['name']}->{category[1]}</b>\n\n"
                                  f"Опишите проблему:")


@router.message(UserOrder.problem)
async def verification_code_user(message: Message, state: FSMContext, db) -> None:
    """
    Register user
    """
    uuid = message.from_user.id
    person = await tool.get_user(str(uuid), db)
    await state.update_data(problem=message.text)
    data = await state.get_data()
    await send_problem(data, person)
    await state.clear()
    await message.answer(text="Ваше обращение оптравленно")
