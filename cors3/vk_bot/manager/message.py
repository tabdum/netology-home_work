import sys
sys.path.append('/home/azamat/Desktop/netology-home-work/cors3')
from cfg.vk_api_auth import TOKEN_GROUP
import vk_api
vk_session = vk_api.VkApi(token=TOKEN_GROUP)
vk_apis = vk_session.get_api()
def user_info_meassage(user_id, name, lastname, city, age, url, photo_iter, gender):
    photo_string = ','.join(list(photo_iter))
    string = f'Твое имя и фамилия: {name} {lastname},\nТвой город: {city},\nТвой возраст: {age},\nтвой пол: {gender}\nCсылка на твой профиль:{url},\nTOP3 твоих фото:'
    vk_apis.messages.send(user_id=user_id, attachment=photo_string, random_id=0, message=string)
def recomendate_message(user_id, name, lastname, city, age, url, photo_iter):
    photo_string = ','.join(list(photo_iter))
    string = f'Имя и Фамилия: {name} {lastname},\nГород: {city},\nВозраст: {age},\nCсылка на профиль:{url}\nTOP3 фото:'
    vk_apis.messages.send(user_id=user_id, attachment=photo_string, random_id=0, message=string)
def favorite_message(user_id, name, lastname, url, photo_iter):
    photo_string = ','.join(list(photo_iter))
    string = f'Имя и Фамилия: {name} {lastname},\nCсылка на профиль:{url}\nTOP3 фото:'
    vk_apis.messages.send(user_id=user_id, attachment=photo_string, random_id=0, message=string)
def not_recomendate(user_id):
    mes = 'Извини, для тебя пока нет рекомендаций...'
    vk_apis.messages.send(user_id=user_id, message=mes, random_id=0)





