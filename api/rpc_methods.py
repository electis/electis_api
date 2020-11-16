import requests
from time import sleep

import vk_api
from modernrpc.core import REQUEST_KEY, ENTRY_POINT_KEY, PROTOCOL_KEY, HANDLER_KEY
from modernrpc.core import rpc_method


def exists(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok


def two_factor():
    code = input('Code? ')
    remember_device = True
    return code, remember_device

# facebook
# https://proglib.io/p/facebook-bot-with-python/
# https://qna.habr.com/q/404019

@rpc_method(name='ok')
def ok_send():
    # https://apiok.ru/dev/methods/rest/mediatopic/mediatopic.post
    # https://github.com/needkirem/ok_api
    return

@rpc_method(name='vk')
def vk_send(owner_id, text, pict, token):
    vk_session = vk_api.VkApi(token=token)
    # vk_session = vk_api.VkApi(login, password, auth_handler=two_factor)
    # try:
    #     vk_session.auth()
    # except vk_api.AuthError as exc:
    #     return exc
    # https://github.com/python273/vk_api/blob/master/examples/auth_by_code.py
    # print(vk_session.token)

    if not exists(pict):
        pict = None

    vk = vk_session.get_api()
    # https://ru.stackoverflow.com/questions/528715/%D0%9F%D0%BE%D1%81%D1%82%D0%B8%D0%BD%D0%B3-%D0%B2-vk-%D1%87%D0%B5%D1%80%D0%B5%D0%B7-vk-api-python
    result = vk.wall.post(message=text, attachments=pict, owner_id=owner_id)
    # result = vk.wall.get(owner_id=owner_id)
    return result



@rpc_method(name='test4async')
def test4async(a, b, **kwargs):
    """
    a + b
    :param a: int
    :param b: int
    :return: int
    """
    # protocol = kwargs.get(PROTOCOL_KEY)
    # entry_point = kwargs.get(ENTRY_POINT_KEY)
    # handler = kwargs.get(HANDLER_KEY)
    # request = kwargs.get(REQUEST_KEY)
    # TODO async for list request
    sleep(a+b)
    return a+b
