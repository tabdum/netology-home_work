import vk_api
from loguru import logger
TOKEN_USER = ''
TOKEN_GROUP = ''
if TOKEN_USER == '' or TOKEN_GROUP == '':
    logger.warning('Файл "vk_api_auth" не заполнен!\nВыполните ручную аутентификацию...')
    TOKEN_USER = input('Введите токен юзера: ').strip()
    TOKEN_GROUP = input('Введите токен группы: ').strip()
VK_SESSION = vk_api.VkApi(token=TOKEN_USER)
VK_API = VK_SESSION.get_api()
param_dict_photo = {
    'owner_id': None,
    'album_id': 'wall',
    'extended': '1'
}