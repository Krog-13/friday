from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def get_reg_bt() -> InlineKeyboardMarkup:
    """
    Registration button
    """
    kb = InlineKeyboardBuilder()
    reg_bt = InlineKeyboardButton(text="Зарегистрироваться 🔵", callback_data="reg")
    cancel_bt = InlineKeyboardButton(text="Обратная связь 🗳", callback_data="cancel")
    kb.add(reg_bt)
    kb.add(cancel_bt)
    kb.adjust(1)
    return kb.as_markup()


def get_lang_bt() -> InlineKeyboardMarkup:
    """
    Language button
    """
    kb = InlineKeyboardBuilder()
    lang_ru = InlineKeyboardButton(text="Русский🇷🇺", callback_data="lang_ru_Русский")
    lang_kz = InlineKeyboardButton(text="Казахский🇰🇿", callback_data="lang_kz_Казахский")
    lang_eng = InlineKeyboardButton(text="Английский🏴󠁧󠁢󠁥󠁮󠁧󠁿", callback_data="lang_eng_Английский")
    kb.add(lang_ru)
    kb.add(lang_kz)
    kb.add(lang_eng)
    return kb.as_markup()


def get_checkin_kb() -> InlineKeyboardMarkup:
    """
    Confirm button
    """
    kb = InlineKeyboardBuilder()
    kb.button(text="Подтвердить ✅", callback_data="check_confirm")
    kb.button(text="Заполнить заново ⭕", callback_data="check_cancel")
    return kb.as_markup()


def get_code_kb() -> InlineKeyboardMarkup:
    """
    Confirm button for code verification
    """
    kb = InlineKeyboardBuilder()
    kb.button(text="Заполнить заново ⭕", callback_data="reset")
    return kb.as_markup()


def get_service_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Новый запрос")
    kb.button(text="Обратная связь")
    kb.button(text="Профиль")
    kb.button(text="🏡 Вернуться на главную")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)


def get_update_kb() -> InlineKeyboardMarkup:
    """
    Update button profile
    """
    kb = InlineKeyboardBuilder()
    kb.button(text="Обновить профиль 📝", callback_data="profile_update")
    return kb.as_markup()


def get_update_profile_kb() -> InlineKeyboardMarkup:
    """
    Update buttons profile
    """
    kb = InlineKeyboardBuilder()
    kb.button(text="ФИО 🔹", callback_data="update_fullname")
    kb.button(text="Почта 🔹", callback_data="update_mail")
    kb.button(text="Номер телефона 🔹", callback_data="update_phone")
    kb.button(text="Руководитель 🔹", callback_data="update_manager")
    kb.button(text="Обновить все данные 🔹", callback_data="update_all")
    kb.adjust(2)
    return kb.as_markup()
