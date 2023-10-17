from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_reg_bt() -> InlineKeyboardMarkup:
    """
    Registration button
    """
    kb = InlineKeyboardBuilder()
    reg_bt = InlineKeyboardButton(text="Зарегистрироваться", callback_data="reg")
    cancel_bt = InlineKeyboardButton(text="Нет, спасибо!", callback_data="cancel")
    kb.add(reg_bt)
    kb.add(cancel_bt)
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
    kb.button(text="Подтвердить", callback_data="check_confirm")
    kb.button(text="Заполнить заново", callback_data="check_cancel")
    return kb.as_markup()


def get_code_kb() -> InlineKeyboardMarkup:
    """
    Confirm button for code verification
    """
    kb = InlineKeyboardBuilder()
    kb.button(text="Заполнить заново", callback_data="reset")
    return kb.as_markup()
