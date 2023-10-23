import tool
import base64
from urllib.parse import quote
from config import logger
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiohttp.web_request import Request
from aiogram.fsm.state import State, StatesGroup
from keyboards.register import get_reg_bt
from keyboards.service_keyboard import get_inet_bt, get_category_bt, get_photo_bt
from filters.chat_type import ChatTypeFilter
from handlers.handler_tool import CategoryCallbackFactory, send_problem
from aiohttp.web_response import json_response
from aiogram import Bot
router = Router()


@router.message(Command("file"))
async def cmd_dice_in_group(message: Message, db):
    if not await tool.exist_user(str(message.from_user.id), db):
        await message.answer(f"Для использования данного <b>меню</b> (<em>Сервис</em>) "
                             f"необходима регистрация\n",
                             reply_markup=get_reg_bt())
        return True
    await message.answer(f"Здравствуйте, для подписания ecp отправьте подписываемый документ")
    await message.answer(text="https://mgovsign.page.link/&apn=kz.mobile.mgov")


@router.message(F.document)
async def order_photo(message: Message, bot) -> None:
    """
    Document upload
    """
    await bot.download(message.document, destination=f"/tmp/{message.document.file_id}.pdf")
    file = await bot.get_file(message.document.file_id)
    file_path = file.file_path # need code param https://developer.donnoval.ru/urlencode/
    document = await bot.download_file(file_path)
    logger.warning("Open mobile app egov")
    res = f"file_path={file_path}"
    param = quote(res)
    await message.answer(text=f"https://mgovsign.page.link/?link=https://ebb8-92-46-127-106.ngrok.io/mgovSign?{param}&apn=kz.mobile.mgov")


async def get_file_sign(request: Request):
    """
    Document upload
    """
    logger.warning("I AM HERE send json with data file base64")
    file_path = request.query["file_path"]
    bot: Bot = request.app["bot"]
    document = await bot.download_file(file_path)
    data = document.read()
    base64_data = base64.b64encode(data)
    base64_string = base64_data.decode('utf-8')
    response = {
        "signMethod": "CMS_SIGN_DATA",
        "documentToSign": [
            {
                "id": 1,
                "nameRu": "Согласование данных",
                "nameKz": "Каз вариант",
                "nameEn": "Data to access",
                "meta": [
                    {
                        "name": "ИИН",
                        "value": "950113350761"
                    },
                    {
                        "name": "GET",
                        "value": "87472017958"
                    }
                ],
                "document": {
                    "file":{
                        "mime": "@file/pdf",
                        "data": base64_string
                    }
                }
            }
        ]
    }
    return json_response({"name": "test"})
