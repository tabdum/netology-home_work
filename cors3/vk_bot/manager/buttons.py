import sys
sys.path.append('/home/azamat/Desktop/netology-home-work/cors3')
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from cfg.vk_api_auth import TOKEN_GROUP
import vk_api
import emoji

LIKE = emoji.emojize(':heart_with_arrow:', language='en')
NEXT = emoji.emojize(':next_track_button:', language='en')

vk_session = vk_api.VkApi(token=TOKEN_GROUP)
vk_apis = vk_session.get_api()

def ancet_button(user_id):
    keyboard_ancet = VkKeyboard(one_time=True)
    keyboard_ancet.add_button('Заполнить анкету!', color=VkKeyboardColor.POSITIVE)
    mes = 'Отлично, теперь чтобы начать знакомства, нам нужно заполнить вашу анкету...'
    vk_apis.messages.send(user_id=user_id, message=mes, random_id=0, keyboard=keyboard_ancet.get_keyboard())
def rec_start_button(user_id):
    keyboard_start_recomendate = VkKeyboard(one_time=True)
    keyboard_start_recomendate.add_button('Смотреть рекомендации!', color=VkKeyboardColor.POSITIVE)
    mes = '\nСупер,твоя анкета готова! У нас уже готовы для тебя рекомендации, хочешь посмотреть?'
    vk_apis.messages.send(user_id=user_id, message=mes, random_id=0, keyboard=keyboard_start_recomendate.get_keyboard())
def rec_button_old_user(user_id):
    keyboard_start_recomendate = VkKeyboard(one_time=True)
    keyboard_start_recomendate.add_button('Вернуться к рекомендациям!', color=VkKeyboardColor.POSITIVE)
    keyboard_start_recomendate.add_button('Избранные', color=VkKeyboardColor.POSITIVE)
    mes = 'Мы уже заждались тебя, у нас для тебя новые рекомендации, хочешь посмотреть?'
    vk_apis.messages.send(user_id=user_id, message=mes, random_id=0, keyboard=keyboard_start_recomendate.get_keyboard())
def rec_buttons(user_id):
    keyboard_recomendate_buttons = VkKeyboard(one_time=True)
    keyboard_recomendate_buttons.add_button(NEXT, color=VkKeyboardColor.POSITIVE)
    keyboard_recomendate_buttons.add_button(LIKE, color=VkKeyboardColor.POSITIVE)
    keyboard_recomendate_buttons.add_button('Избранные', color=VkKeyboardColor.POSITIVE)
    vk_apis.messages.send(user_id=user_id, random_id=0, keyboard=keyboard_recomendate_buttons.get_keyboard(), message='Выберите действие')
def recomendate_finaly(user_id):
    keyboard_recomendate_fin = VkKeyboard(one_time=True)
    keyboard_recomendate_fin.add_button('Избранные', color=VkKeyboardColor.POSITIVE)
    mes = 'На сегодня рекомендации закончились, заходи к нам позже...'
    vk_apis.messages.send(user_id=user_id, message=mes, random_id=0, keyboard=keyboard_recomendate_fin.get_keyboard())
def access_favorite_message(user_id, name, lastname):
    keyboard_start_recomendate = VkKeyboard(one_time=True)
    keyboard_start_recomendate.add_button('Рекомендации', color=VkKeyboardColor.POSITIVE)
    keyboard_start_recomendate.add_button('Избранные', color=VkKeyboardColor.POSITIVE)
    mes = f'{name} {lastname} успешно добавлен(а) в твой список избранных'
    vk_apis.messages.send(user_id=user_id, message=mes, random_id=0, keyboard=keyboard_start_recomendate.get_keyboard())
def return_for_rec(user_id, mes=''):
    keyboard_return_rec = VkKeyboard(one_time=True)
    keyboard_return_rec.add_button('Рекомендации', color=VkKeyboardColor.POSITIVE)
    vk_apis.messages.send(user_id=user_id, random_id=0, message=mes, keyboard=keyboard_return_rec.get_keyboard())
