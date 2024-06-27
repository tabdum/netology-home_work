import sys
sys.path.append('/home/azamat/Desktop/netology-home-work/cors3')
from database.database_class import *
from manager.manager_main import Manager, LONGPOOL, VkEventType
from manager.buttons import LIKE, NEXT
#--------------------------------------------------------------------------------------------------------------------------------------
DataBase.create_db() 
example_vk_ids = ['505187581', '464883336', '183381878', '299944791',
                 '844952901', '352286718', '186811160', '241937855', 
                 '146438077', '217777594', '246870728', '210796238']
for i in example_vk_ids:
    try:
        user = DataBase(vk_id=i)
        user.add_user()
    except ValueError:
        continue
#----------------------------------------------------------------------------------------------------------------------------------------
for event in LONGPOOL.listen():
    boolin1 = event.type == VkEventType.MESSAGE_NEW
    boolin2 = event.to_me
    its_new_message = all([boolin1, boolin2])
    if its_new_message:
        user_manager = Manager(event)
        if event.text.lower() == 'start':
            user_manager.start()
        if event.text == 'Заполнить анкету!':
            user = DataBase(vk_id=str(event.user_id))
            user_manager.fill_ancet(user)
        if event.text == 'Смотреть рекомендации!' or event.text == 'Рекомендации':
            rec = user_manager.get_first_rec(user)
        if event.text == NEXT:
            rec = user_manager.next_rec(user)
        if event.text == LIKE:
            user_manager.add_to_favorites(user, rec)
        if event.text == 'Избранные':
            user_manager.get_favorites_list(user)