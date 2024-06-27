from loguru import logger
DATABASE = ''
USER = ''
PASSWORD = ''
photo_dict_lecal = {
    'link_photo1': None,
    'link_photo2': None,
    'link_photo3': None
}
if DATABASE == '' or USER == '' or PASSWORD == '':
    logger.warning('Файл конфигурации "database_config" не заполнен!\nВыполните ручную аутентификацию...')
    DATABASE = input('Введите базу данных к которой хотите подключиться: ').strip()
    USER = input('Введите пользователя: ').strip()
    PASSWORD = input('Введите пароль: ').strip()