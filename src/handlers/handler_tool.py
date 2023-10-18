from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib
from aiogram.filters.callback_data import CallbackData
from typing import Optional
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, logger


class CategoryCallbackFactory(CallbackData, prefix="network"):
    action: str
    name: str
    description: Optional[str] = None
    value_id: Optional[int] = None


async def preset_data(data):
    """
    Personal data for registration
    """
    if data["user_language"] == "ru":
        data["user_language"] = "Русский"
    elif data["user_language"] == "kz":
        data["user_language"] = "Казахский"
    elif data["user_language"] == "eng":
        data["user_language"] = "Английский"

    result = f"""<u>Ваши данные:</u>
        <b>ФИО:</b> {data['fullname']}
        <b>Почта:</b> {data['email']}
        <b>Номер телефона:</b> {data['phone']}
        <b>Рукаводитель:</b> {data['manager']}
        <b>Язык интерфейса:</b> {data['user_language']}
    """
    return result


async def send_code_verification(email, code):
    """
    Account verification
    """
    try:
        sender_email = EMAIL_HOST_USER
        password = EMAIL_HOST_PASSWORD

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = 'Верификация аккаунта сотрутника KMG'

        html = f"""\
            <html>
              <body>
                <h4>Вас приветствует SMART BOT 'КазМунайГаз'</h4>
                <em>Код верификации - <b>{code}</b></em>                       
              </body>
            </html>
            """
        msg.attach(MIMEText(html, 'html'))
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
            logger.warning(f"Code verification send by email {email}")
            smtp.starttls()
            smtp.login(sender_email, password)
            smtp.sendmail(sender_email, email, msg.as_string())
        return 0
    except Exception as e:
        logger.error(f"Ошибка отправки почты {e}")


async def send_problem(data, person, photo=None):
    """
    Account verification
    """
    email = "a.nurkin@kmg.kz"
    # email = "r.nazarova@kmg.kz"
    try:
        sender_email = EMAIL_HOST_USER
        password = EMAIL_HOST_PASSWORD

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = 'Верификация аккаунта сотрутника KMG'
        html = f"""\
            <html>
            <body>
              <h4>Категория</h4> - <em>{data["name"]}</em>
              <h4>Подкатегория</h4> - <em>{data["subcategory"]}</em>
                <h5>Описание проблемы</h5> <p>{data["problem"]}</p>
                <br>  
                <h5>Автор обращения: {person[5]}</h5>                     
                <h5>Рукаводитель:  <em>{person[6]}</em></h5>           
                <h5>Телефон: <em>{person[3]}</em></h5>                     
            </body>
            </html>
            """
        msg.attach(MIMEText(html, 'html'))
        if photo:
            msg.attach(MIMEImage(photo.read(), name='photo.jpg'))
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
            logger.warning(f"Problem sended {email}")
            smtp.starttls()
            smtp.login(sender_email, password)
            smtp.sendmail(sender_email, email, msg.as_string())
        return 0
    except Exception as e:
        logger.error(f"Ошибка отправки почты {e}")
