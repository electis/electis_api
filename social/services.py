'''
social services, class name = service name, methods: post, ...
'''
import requests
import vk_api


def url_exists(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok


class VK:
    def post(self, token, owner, text=None, pict=None):
        vk_session = vk_api.VkApi(token=token)
        if not url_exists(pict):
            pict = None
        vk = vk_session.get_api()
        result = vk.wall.post(message=text, attachments=pict, owner_id=owner)
        return result

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
            return exc
        token = vk_session.token
        # result = vk.wall.get(owner_id=owner_id)
        # print(vk_session.token)