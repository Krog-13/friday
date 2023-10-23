import tool
import base64

from urllib.parse import quote
from config import logger, APP_BASE_URL
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router, F
from aiohttp.web_request import Request
from aiogram.fsm.context import FSMContext
from keyboards.register import get_reg_bt
from aiohttp.web_response import json_response
from aiogram import Bot
router = Router()


class FileSate(StatesGroup):
    """
    Personal data
    """
    document = State()


@router.message(Command("file"))
async def cmd_dice_in_group(message: Message, state: FSMContext, db):
    if not await tool.exist_user(str(message.from_user.id), db):
        await message.answer(f"Для использования данного <b>меню</b> (<em>Сервис</em>) "
                             f"необходима регистрация\n",
                             reply_markup=get_reg_bt())
        return True
    await state.set_state(FileSate.document)
    await message.answer(f"Здравствуйте, для подписания ecp отправьте подписываемый документ")

@router.message(FileSate.document)
# @router.message(F.document)
async def order_photo(message: Message,state: FSMContext, bot) -> None:
    """
    Document upload
    """
    await bot.download(message.document, destination=f"/tmp/{message.document.file_id}.pdf")
    file = await bot.get_file(message.document.file_id)
    file_path = file.file_path  # need code param https://developer.donnoval.ru/urlencode/
    logger.warning("Open mobile app egov")
    res = f"file_path={file_path}"
    param = quote(res)
    await state.clear()
    await message.answer(text=f"https://mgovsign.page.link/?link={APP_BASE_URL}/mgovSign?{param}&apn=kz.mobile.mgov")


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
    return json_response(response)
