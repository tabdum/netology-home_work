import sys
sys.path.append('/home/azamat/Desktop/netology-home-work/cors3')
from loguru import logger
from database.database_class import *
import manager.message as message
from manager.buttons import *
from cfg.vk_api_auth import TOKEN_GROUP
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
logger.add('log/war.log', format="{time} {level} {message}", level='WARNING')
logger.add('log/err.log', format="{time} {level} {message}", level='ERROR')
logger.add('log/info.log', format="{time} {level} {message}", level='INFO')

vk_session = vk_api.VkApi(token=TOKEN_GROUP)
vk_apis = vk_session.get_api()
LONGPOOL = VkLongPoll(vk_session)

class Manager:
    def __init__(self, event):
        self._event = event
    @property
    def event(self):
        return self._event
    @event.setter
    def event(self):
        raise AttributeError('Нельзя вносить изменения в цикл событий')
    def start(self):
        event = self.event
        logger.info(f'Пользователь с vk_id {event.user_id} прописал "start"')
        if DataBase.vk_id_check(event.user_id) is False:
            logger.info(f'Пользователю с vk_id {event.user_id} отправлена к нопка на заполнение отправлена')
            ancet_button(event.user_id)
        else:
            rec_button_old_user(event.user_id)
    def fill_ancet(self, user):
        event = self.event
        logger.info(f'Пользователь с vk_id {event.user_id} нажал кнопку: "Заполнить анкету!"')
        user.add_user()
        logger.info(f'Пользователь с vk_id {event.user_id} добавлен в базу данных')
        u_d = user.user_info
        message.user_info_meassage(user_id=event.user_id, name=u_d['name'], 
                                lastname=u_d['lastname'], city=u_d['city'], 
                                age=u_d['age'], url=u_d['url'], 
                                photo_iter=u_d['photo_iter'], gender=u_d['gender'])
        rec_start_button(event.user_id)
        logger.info(f'Пользователю с vk_id {event.user_id} отправлена кнопка рекомендаций')
    def get_first_rec(self, user):
        event = self.event
        try:
            i = next(user.recomendate)
            logger.info(f'Пользователь с vk_id {event.user_id} нажал кнопку просмотра рекомендаций')
            message.recomendate_message(user_id=event.user_id, name=i['name'], 
                                        lastname=i['lastname'], city=i['city'], 
                                        age=i['age'], url=i['url'], 
                                        photo_iter=i['photo_iter'])
            logger.info(f'Пользователю с vk_id {event.user_id} отправлен в качестве рекомендации юзер с vk_id {1}')
            rec_buttons(event.user_id)
            logger.info(f'Пользователю с vk_id {event.user_id} отправлены кнопки управления рекомендациями')
            return i
        except ValueError:
            message.not_recomendate(event.user_id)
        except StopIteration:
            logger.warning(f'Для пользователя с vk_id {event.user_id} закончились рекомендации')
            recomendate_finaly(event.user_id)
    def next_rec(self, user):
        event = self.event
        try:
            i = next(user.recomendate)
            message.recomendate_message(user_id=event.user_id, name=i['name'], 
                                        lastname=i['lastname'], city=i['city'], 
                                        age=i['age'], url=i['url'], 
                                        photo_iter=i['photo_iter'])
            logger.info(f'Пользователю с vk_id {event.user_id} отправлена рекомендация')
            rec_buttons(event.user_id)
            return i
        except StopIteration:
            logger.warning(f'Для пользователя с vk_id {event.user_id} закончились рекомендации')
            recomendate_finaly(event.user_id)
    def add_to_favorites(self, user, rec):
        event = self.event
        try:
            user.add_user_favorite(favorite_vk_id=rec['vk_id'])
            access_favorite_message(event.user_id, rec['name'], rec['lastname'])
        except ValueError:
            logger.warning(f'Пользователь с vk_id {event.user_id} пытался добавить юзера в избранное, который уже числится в списке его избранных')
    def get_favorites_list(self, user):
        event = self.event
        try:
            for i in user.favorites:
                message.favorite_message(user_id=event.user_id, name=i['name'], 
                                        lastname=i['lastname'], url=i['url'], photo_iter=i['photo_iter'])
            else:
                logger.info(f'Пользователю с vk_id {event.user_id} отправлен лист избранных')
                return_for_rec(event.user_id, mes='Выберете действие')
        except ValueError:
            return_for_rec(event.user_id, mes='Твой список избранных пуст')