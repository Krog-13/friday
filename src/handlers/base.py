from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram import Router, F
from filters.chat_type import ChatTypeFilter
from aiogram.fsm.context import FSMContext
import tool
import random
from .handler_tool import send_code_verification
from aiogram.fsm.state import State, StatesGroup
from .registration import checkin_confirm
from config import BASE_DIR, logger
from keyboards.register import get_reg_bt, get_service_kb, get_update_kb, get_update_profile_kb

router = Router()
router.message.filter(ChatTypeFilter(chat_type=["group", "supergroup"]))
_KMG_LOGO = FSInputFile(BASE_DIR + "/media/logo_kmg.jpg")


class UserStates(StatesGroup):
    """
    Personal data
    """
    dataUpdate = State()
    codes = State()


@router.message(CommandStart())
async def cmd_dice_in_group(message: Message, db):
    user = await tool.exist_user(str(message.from_user.id), db)

    if not user:
        logger.warning("New user to want registration")
        await message.answer_photo(_KMG_LOGO, caption="Вас приветствует Смарт-бот 🐹'КазМунайГаз'\n"
                                                      "для дальнейшего пользования Вам необходимо "
                                                      "<b>зарегистрироваться</b> 🔵", reply_markup=get_reg_bt())
        return True

    await message.answer_photo(photo=_KMG_LOGO,
                               caption=f"Здравствуйте 🐏 <u>{user[0]}</u> \nВас приветствует Смарт-бот 'КзаМунайГаз'🐹\n"
                                       f"Личные данные:\n"
                                       f"▫ Почта: ✉ - {user[1]}\n"
                                       f"▫ Номер телефона: ☎ - {user[2]}\n"
                                       f"▫ Руководитель: 🐼 - {user[3]}", reply_markup=get_service_kb())


@router.message(Command("help"))
async def helper(message: Message):
    await message.answer(f"Здравствуйте Вас приветствует Смарт-бот 🐹'КазМунайГаз'\n"
                         f"Доступные комманды: 📎\n"
                         f"▫ Начало /start\n"
                         f"▫ Регистрация /register\n"
                         f"▫ Новый запрос /service\n"
                         f"▫ Сброс /cancel")


@router.message(Command("cancel"))
async def canceled_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Сброс")


@router.message(F.text.startswith("Профиль"))
async def canceled_command(message: Message, db):
    user = await tool.exist_user(str(message.from_user.id), db)
    if not user:
        logger.warning("New user to want registration")
        await message.answer_photo(_KMG_LOGO, caption="Вас приветствует Смарт-бот 🐹'КазМунайГаз'\n"
                                                      "для дальнейшего пользования Вам необходимо "
                                                      "<b>зарегистрироваться</b> 🔵", reply_markup=get_reg_bt())
        return
    await message.answer(f"Здравствуйте 🐑 <u>{user[0]}</u>, \nВаш профиль 📔\n\n"
                         f"Почта: ✉ - {user[1]}\n"
                         f"Номер телефона: ☎ - {user[2]}\n"
                         f"Руководитель: 🐼 - {user[3]}", reply_markup=get_update_kb())


@router.message(F.text.startswith("Обратная"))
async def canceled_command(message: Message):
    await message.answer("🗳 При возникновени вопросов, просим обращаться по нижеуказанным контактам:\n"
                         "<em>с городского телефона</em>: ☎ - <b>1444</b>\n"
                         "<em>с мобильного телефона</em>: ☎ - <b>+7(800)-080-1444</b>\n"
                         "<em>Почта</em>: ✉ - <b>sms@kmg.kz</b>")


@router.callback_query(F.data.startswith("profile_"))
async def checkin_lang(callback: CallbackQuery) -> None:
    """
    Update profile
    """
    await callback.answer("Обновление профиля! 📔", show_alert=False)

    await callback.message.answer("Выбирите пункт обновления 🔁", reply_markup=get_update_profile_kb())


@router.callback_query(F.data.startswith("update_"))
async def checkin_lang(callback: CallbackQuery, state: FSMContext, bot) -> None:
    """
    Update profile
    """
    await callback.answer("Обновление профиля", show_alert=False)

    part_profile = callback.data.split("_")[1]
    if part_profile == "all":
        await checkin_confirm(callback, state, bot)
    elif part_profile == "mail":
        await state.set_state(UserStates.dataUpdate)
        await callback.message.answer("Введите новую корпаративную почту ✉:")


@router.message(UserStates.dataUpdate)
async def process_email(message: Message, state: FSMContext, db) -> None:
    """
    Email validation
    """
    code = random.randrange(1000, 10000)
    await state.update_data(codes=str(code))
    if not message.entities or message.entities[0].type != "email":
        await message.answer("Не корректный формат почты 🚫")
        return
    elif message.text.rsplit("@")[1].rfind("kmg") == -1:
        await message.answer("Необходимо указать корпоративную почту ✉")
        return
    await send_code_verification(message.text, code)
    await message.answer(f"Введите код верификации 🔑, отправленный на почту ✉ <i>{message.text}</i>")
    await state.update_data(dataUpdate=message.text)
    await state.set_state(UserStates.codes)


@router.message(UserStates.codes)
async def verification_code_user(message: Message, state: FSMContext, db) -> None:
    """
    Register user
    """
    data = await state.get_data()
    if data['codes'] == message.text:
        await tool.email_update(user_id=message.from_user.id, email=data["dataUpdate"], db=db)
        await state.clear()
        logger.warning(f"User by email {data['dataUpdate']} was registered")
        await message.answer("Ваша почта успешно изменена! ✅", reply_markup=get_service_kb())
    else:
        logger.warning(f"User by email {data['dataUpdate']} enter incorrect verify code")
        await message.answer("Код верификации неверный 🚫, убедитесь в корректности кода и введите еще раз!")
