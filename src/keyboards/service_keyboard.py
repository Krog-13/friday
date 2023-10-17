from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from typing import Optional
from handlers.handler_tool import CategoryCallbackFactory


def get_category_bt(db):
    """
    """
    category = db.category_parent()
    builder = InlineKeyboardBuilder()
    for cat in category:
        builder.button(text=cat[1], callback_data=CategoryCallbackFactory(action="change", value_id=cat[0], name=cat[1]))
    builder.adjust(4)
    return builder.as_markup()


def get_servie_bt(db) -> ReplyKeyboardMarkup:
    """
    Category button
    """
    category = db.category_parent()
    kb = [[KeyboardButton(text=i[1], callback_data="test")] for i in category]
    # one_time_keyboard после нажатия скрывает кнопки
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                         input_field_placeholder="select what do you need", one_time_keyboard=True)
    return keyboard


def get_inet_bt(sub_cat, name) -> InlineKeyboardMarkup:
    """
    Ca
    """
    kb = InlineKeyboardBuilder()
    for cat in sub_cat:
        kb.button(text=cat[1], callback_data=f"fix_{cat[1]}_{cat[0]}")
    return kb.as_markup()
