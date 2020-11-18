'''
social services, class name = service name, methods: post, ...
'''
from abc import ABC, abstractmethod
from typing import Union

import requests
import vk_api
from benedict import benedict


def url_exists(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok


class ServiceFactory(ABC):
    @abstractmethod
    def post(self, token, owner, text=None, pict=None) -> Union[int, str, None]:
        '''
        post message to social service
        :param token: access token
        :param owner: group or user id
        :param text: message text
        :param pict: message picture
        :return: post_id or None
        '''
        pass

    @abstractmethod
    def auth(self, login, password) -> str:
        '''
        provide auth in social service
        :param login:
        :param password:
        :return: access token
        '''
        pass


class VK(ServiceFactory):
    def post(self, token, owner, text=None, pict=None):
        vk_session = vk_api.VkApi(token=token)
        if not url_exists(pict):
            pict = None
        vk = vk_session.get_api()
        result = vk.wall.post(message=text, attachments=pict, owner_id=owner)
        # d = benedict(result).get_str(data_fields['post_id'])
        if result and 'post_id' in result:
            return result['post_id']

    @staticmethod
    def two_factor():
        code = input('Code? ')
        remember_device = True
        return code, remember_device

    def auth(self, login, password):
        # https://github.com/python273/vk_api/blob/master/examples/auth_by_code.py
        # https://ru.stackoverflow.com/questions/528715/%D0%9F%D0%BE%D1%81%D1%82%D0%B8%D0%BD%D0%B3-%D0%B2-vk-%D1%87%D0%B5%D1%80%D0%B5%D0%B7-vk-api-python
        vk_session = vk_api.VkApi(login, password, auth_handler=VK.two_factor)
        try:
            vk_session.auth()
        except vk_api.AuthError as exc:
            raise
        token = vk_session.token
        # result = vk.wall.get(owner_id=owner_id)
        # print(vk_session.token)
        return token
