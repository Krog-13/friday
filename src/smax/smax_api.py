from config import API_SMAX_URL, API_SMAX_URL_TOKEN
from .helper import prepare_post_params, get_id_order
import requests

# skip warning ssl certification
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



TOKEN = None
_HEADERS = {
    "Content-Type": "application/json",
    "Cookie": None
}


async def send_message_smax(data, user):
    """
    POST query smax
    create new query oneline
    """
    _is_valid = await _valid_token()
    if not _is_valid:
        _HEADERS.update(Cookie=TOKEN)
    query_param = await prepare_post_params(data, user)
    try:
        response = requests.post(f"{API_SMAX_URL}/bulk", headers=_HEADERS, json=query_param, verify=False)
        return await get_id_order(response.json())
    except requests.exceptions.HTTPError as err:
        print(err.args[0])


async def get_status_smax(order_id):
    """
    GET query smax
    status
    """
    _is_valid = await _valid_token()
    if not _is_valid:
        _HEADERS.update(Cookie=TOKEN)
    query_param = {
        "layout": "Id,PhaseId,Active,Description"
    }
    try:
        response = requests.get(f"{API_SMAX_URL}/Request/{order_id}", headers=_HEADERS, params=query_param, verify=False)
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(err.args[0])


async def _valid_token():
    """
    Accept new token
    :return token
    """
    try:
        response = requests.post(API_SMAX_URL, headers=_HEADERS, verify=False)
        if response.status_code != 401:
            return True
    except requests.exceptions.HTTPError as err:
        print(err.args[0])

    global TOKEN
    query_param = {"TENANTID": 855226221}
    body_param = {"login": "telegrambot", "password": "Astana2023!"}
    try:
        response = requests.post(API_SMAX_URL_TOKEN, json=body_param, params=query_param, verify=False)
        TOKEN = "SMAX_AUTH_TOKEN="+response.text
        return
    except requests.exceptions.HTTPError as err:
        print(err.args[0])
