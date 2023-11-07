import tool
from config import logger
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.register import get_reg_bt, get_lang_bt, get_checkin_kb, get_code_kb, get_service_kb
from filters.chat_type import ChatTypeFilter
from .handler_tool import preset_data, send_code_verification
import random


router = Router()
router.message.filter(ChatTypeFilter(chat_type=["group", "supergroup"]))


class UserStates(StatesGroup):
    """
    Personal data
    """
    fullname = State()
    phone = State()
    email = State()
    user_language = State()
    manager = State()
    code = State()


@router.message(Command("register"))
async def register_person(message: Message, db):
    user = await tool.exist_user(str(message.from_user.id), db)
    if not user:
        logger.warning("New user to want registration")
        await message.answer(f"Здравствуйте Вас привествует смарт-бот 'КазМунайГаз'"
                             f"для регистрации нажмите соответствующую кнопку\n", reply_markup=get_reg_bt())
        return True
    await message.answer(f"Здравствуйте 🐏 <u>{user[0]}</u>, \nВы уже зарегистрированный пользователь!\n"
                         f"Личные данные:\n"
                         f"Почта ✉ - {user[1]}\n"
                         f"Номер телефона ☎ - {user[2]}\n"
                         f"Руководитель 🐼 - {user[3]}", reply_markup=get_service_kb())


@router.callback_query(F.data == "reg")
async def checkin_confirm(callback: CallbackQuery, state: FSMContext, bot) -> None:
    # registration
    await bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=None)

    await callback.answer("Для регистрации укажите 📝:\n\nФИО 🐏\nКорпаративную почту ✉\nНомер телефона ☎\nНепосредственного руководителя 🐼\nЯзык интерфейса 🌏", show_alert=True)
    await callback.message.answer("Введите ФИО 🐏:", reply_markup=None)
    await state.set_state(UserStates.fullname)


@router.callback_query(F.data == "cancel")
async def canceled(callback: CallbackQuery, bot) -> None:
    # cancel
    await bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=None)

    await callback.answer()
    await callback.message.answer("🗳 При возниконовени вопросов, просим обращаться по нижеуказанным контактам:\n"
                         "<em>Tелефон ☎:</em> <b>1414</b>\n"
                         "<em>Почта ✉:</em> <b>manager@kmg.kz</b>")


@router.message(UserStates.fullname)
async def process_name(message: Message, state: FSMContext) -> None:
    """
    User's full name
    """
    await state.update_data(fullname=message.text)
    await state.set_state(UserStates.email)
    await message.answer("Введите Вашу корпаративную почту ✉:")


@router.message(UserStates.email)
async def process_email(message: Message, state: FSMContext) -> None:
    """
    Email validation
    """
    if not message.entities or message.entities[0].type != "email":
        await message.answer("Не корректный формат почты 🚫")
        return
    elif message.text.rsplit("@")[1].rfind("kmg") == -1:
        await message.answer("Необходимо указать корпоративную почту ✉")
        return
    await state.update_data(email=message.text)
    await state.set_state(UserStates.phone)
    await message.answer("Введите Ваш номер телефона ☎ (должен содержать только цифры):")


@router.message(UserStates.phone)
async def process_manager(message: Message, state: FSMContext) -> None:
    """
    User's phone
    """
    if not message.text.isdigit():
        await message.answer("Не корректный формат телефона 🚫")
        return
    await state.update_data(phone=message.text)
    await state.set_state(UserStates.manager)
    await message.answer("Введите ФИО Вашего рукаводителя 🐼:")


@router.message(UserStates.manager)
async def process_manager(message: Message, state: FSMContext) -> None:
    """
    User's manager
    """
    await state.update_data(manager=message.text)
    await state.set_state(UserStates.user_language)
    await message.answer("Выбирете язык интерфейса 🌏:", reply_markup=get_lang_bt())


@router.callback_query(F.data.startswith("lang_"), UserStates.user_language)
async def checkin_lang(callback: CallbackQuery, state: FSMContext, bot) -> None:
    """
    Parse selected lang
    """
    await bot.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=None)
    lang_msg = callback.data.split("_")[2]
    lang_code = callback.data.split("_")[1]
    await callback.answer()
    await callback.message.answer(f"Язык интерфейса {lang_msg}")
    await state.update_data(user_language=lang_code)

    data = await state.get_data()
    personal_data = await preset_data(data=data)
    await callback.message.answer(text=personal_data, reply_markup=get_checkin_kb())


@router.callback_query(F.data.startswith("check_"), UserStates.user_language)
async def verification_user(callback: CallbackQuery, state: FSMContext, bot) -> None:
    """
    Confirming
    """
    code = random.randrange(1000, 10000)
    await state.update_data(code=str(code))
    data = await state.get_data()
    confirm = callback.data.split("_")[1]
    await callback.answer()
    if confirm == "confirm":
        await send_code_verification(data["email"], code)
        await callback.message.answer(f"Введите код верификации 🔑, отправленный на почту ✉ <i>{data['email']}</i>")
        await state.set_state(UserStates.code)
    else:
        await callback.message.answer("* <i>Заполните данные заново 📝</i> *")
        await checkin_confirm(callback, state, bot)


@router.message(UserStates.code)
async def verification_code_user(message: Message, state: FSMContext, db) -> None:
    """
    Register user
    """
    data = await state.get_data()
    if data['code'] == message.text:
        await tool.add_user(data=data, user_uid=message.from_user.id, db=db)
        await state.clear()
        logger.warning(f"User by email {data['email']} was registered")
        await message.answer("Поздравлеям Вы зарегистрировались! 🟢", reply_markup=get_service_kb())
    else:
        logger.warning(f"User by email {data['email']} enter incorrect verify code")
        await message.answer("Код верификации неверный 🚫, убедитесь в корректности кода и введите еще раз!",
                             reply_markup=get_code_kb())


@router.callback_query(F.data.startswith("reset"), UserStates.code)
async def canceled(callback: CallbackQuery, state: FSMContext, bot) -> None:
    """
    Restart registration
    """
    await callback.answer()
    await state.clear()
    await callback.message.answer("* <i>Заполните данные заново 📝</i> *")
    await checkin_confirm(callback, state, bot)


@router.message(Command("cancel"))
async def canceled_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Сброс")
