import sys
sys.path.append('/home/azamat/Desktop/netology-home-work/cors3')
from cfg.database_config import *
from cfg.vk_api_auth import VK_API, VK_SESSION, param_dict_photo
import psycopg2
from datetime import datetime
import re
from itertools import zip_longest
class DataBase:
    _database = DATABASE
    _user = USER
    _password = PASSWORD
    @classmethod
    def create_db(cls):
        conn = psycopg2.connect(database=cls._database, user=cls._user, password=cls._password)
        with conn.cursor() as cur:
            cur.execute("""
                            DROP TABLE IF EXISTS photo_top3;
                            DROP TABLE IF EXISTS Favorites_list;
                            DROP TABLE IF EXISTS Ident;
                            CREATE TABLE IF NOT EXISTS Ident(
                                id_db bigint UNIQUE NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 98765323232),
                                vk_id VARCHAR(50) UNIQUE NOT NULL,
                                name VARCHAR(50) NOT NULL, 
                                lastname VARCHAR(80) NOT NULL,
                                age smallint, 
                                gender VARCHAR(10),
                                city VARCHAR(50)
                            );

                            CREATE TABLE IF NOT EXISTS Favorites_list(
                                id_db bigint REFERENCES Ident(id_db),
                                favorite_id bigint REFERENCES Ident(id_db),
                                CONSTRAINT user_favorite UNIQUE(id_db, favorite_id)
                            );

                            CREATE TABLE IF NOT EXISTS photo_top3(
                                id_db bigint UNIQUE REFERENCES Ident(id_db),
                                link_photo1 VARCHAR(500),
                                link_photo2 VARCHAR(500),
                                link_photo3 VARCHAR(500)	
                            );
                        """)
            conn.commit()   
        conn.close()
        logger.warning('База данных создана (повторное создание приведет к удалению содержимого)\n')
    def __init__(self, vk_id):
        self._id_db = None
        self._vk_id = vk_id
        self._user_info = None
        self._favorites = self.get_favorites()
        self._recomendate = self.get_recommend()
    @property
    def recomendate(self):
        return self._recomendate
    @ recomendate.setter
    def recomendate(self):
        raise AttributeError('Рекомендации подбираются авто-ски, их нельзя изменить вручную')
    @property    
    def id_db(self):
        return self._id_db
    @id_db.setter
    def id_db(self, id_value):
        raise AttributeError('Менять "id_db" запрещено!')
    @property
    def vk_id(self):
        return self._vk_id
    @vk_id.setter
    def vk_id(self, new_id):
        raise AttributeError('Невозможно изменить id пользователя во Вконтакте')
    @property
    def user_info(self):
        return self._user_info
    @user_info.setter
    def user_info(self, new_dict):
        raise AttributeError('''Изменение информации о пользователе в данной реализации неактивна, 
                она берется автоматически из страницы пользователя''')
    @property
    def favorites(self):
        return self.get_favorites()
    @staticmethod
    def get_age(birthday_date:str)->int:
        if re.search(r'\d{4}', birthday_date) is None:
            return None
        else:
            b_d = re.findall(r'(\d+).(\d+).(\d{4})', birthday_date)[0]
            days = (datetime.now() - datetime(year=int(b_d[2]), month=int(b_d[1]), day=int(b_d[0]))).days
            age = days // 365
            return age
    @staticmethod
    def get_gender(number=None)->str:
        if number == 1:
            return 'Жен.'
        if number == 2:
            return 'Муж.'
    @staticmethod
    def fill_attr_info(vk_id:str)->dict:
        info_user = VK_API.users.get(user_id=vk_id, fields='bdate,city,sex')
        dict_info = {
            'vk_id': info_user[0]['id'],
            'name': None,
            'lastname': None,
            'age': None, 
            'gender': None, 
            'city': None
        }
        try:
            dict_info['name'] = info_user[0]['first_name']
        except KeyError:
            pass
        try:
            dict_info['lastname'] = info_user[0]['last_name']
        except KeyError:
            pass
        try:
            dict_info['age'] = DataBase.get_age(info_user[0]['bdate'])
        except KeyError:
            pass
        try:
            dict_info['gender'] = DataBase.get_gender(info_user[0]['sex'])
        except KeyError:
           pass
        try:
            dict_info['city'] = info_user[0]['city']['title']
        except KeyError:
            pass
        return dict_info
    def add_user(self):
        i_d = self.fill_attr_info(self.vk_id)
        try:
            if None in i_d.values():
                no_fill = [i[0] for i in i_d.items() if i[1] is None]
                no_fill_string = ', '.join(no_fill)
                raise ValueError
            conn = psycopg2.connect(database=DataBase._database, user=DataBase._user, password=DataBase._password)
            with conn.cursor() as cur:
                try:    
                    cur.execute("""
                                INSERT INTO Ident(vk_id, name, lastname, age, gender, city)
                                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_db;
                                """, (i_d['vk_id'], i_d['name'].capitalize(), i_d['lastname'].capitalize(), i_d['age'], i_d['gender'], i_d['city']))
                    conn.commit()
                    id_db_value = cur.fetchone()[0]
                    self._id_db = id_db_value
                    conn.close()
                except psycopg2.errors.UniqueViolation:
                    conn.close()
                    logger.error(f'Ошибка! Пользователь c vk_id-({self.vk_id}) был добавлен ранее.')
                    pass
                else:
                    logger.info(f"Успешно! Пользователь c vk_id-({self.vk_id}) добавлен(а) в таблицу 'Ident' по id: {id_db_value}")
                    photo_iter = self.add_top3_photo()
                    i_d['url'] = f'https://vk.com/id{self.vk_id}'
                    i_d['photo_iter'] = photo_iter
                    self._user_info = i_d
                    conn.close()
        except ValueError:
            s = f"Ошибка! У пользователя с vk_id-({self.vk_id}) в профиле ВК не заполнены следующие данные: {no_fill_string}"
            raise ValueError(s)
    def manual_add_user(self, info_dict:dict):
        i_d = info_dict
        conn = psycopg2.connect(database=DataBase._database, user=DataBase._user, password=DataBase._password)
        with conn.cursor() as cur:
            try:    
                cur.execute("""
                            INSERT INTO Ident(vk_id, name, lastname, age, gender, city)
                            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_db;
                            """, (i_d['vk_id'], i_d['name'].capitalize(), i_d['lastname'].capitalize(), i_d['age'], i_d['gender'], i_d['city'].capitalize()))
                conn.commit()
                id_db_value = cur.fetchone()[0]
                self._id_db = id_db_value
                conn.close()
            except psycopg2.errors.UniqueViolation:
                conn.close()
                logger.error(f'Ошибка! Пользователь c vk_id-({self.vk_id}) был добавлен ранее.')
                pass
            else:
                logger.info(f"Успешно! Пользователь c vk_id-({self.vk_id}) добавлен(а) в таблицу 'Ident' по id: {id_db_value}")
                photo_dic = self.add_top3_photo()
                i_d['photo_iter'] = photo_dic
                self._user_info = i_d
                conn.close()
    def add_user_favorite(self, favorite_vk_id:str):
        conn = psycopg2.connect(database=DataBase._database, user=DataBase._user, password=DataBase._password)
        with conn.cursor() as cur:
            cur.execute("SELECT id_db FROM Ident WHERE vk_id = '%s';" % (favorite_vk_id))
            value_favorite = cur.fetchone()
            if value_favorite is not None:
                try:
                    cur.execute("""
                            INSERT INTO Favorites_list(id_db, favorite_id)
                            VALUES (%s, %s);
                            """, (self.id_db, value_favorite))
                    conn.commit()
                    logger.info(f"Человек с vk_id-({favorite_vk_id}) успешно добавлен в избранное пользователя с vk_id-({self.vk_id})")
                    conn.close()
                except psycopg2.errors.UniqueViolation:
                    conn.close()
                    raise ValueError(f'Ошибка! Человек с vk_id - ({favorite_vk_id}) ранее был добавлен в список избранных пользователя')
    def get_favorites(self):
        fav_url = f'https://vk.com/id'
        conn = psycopg2.connect(database=DataBase._database, user=DataBase._user, password=DataBase._password)
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT favorite_id FROM Favorites_list WHERE id_db = %s;" % (self.id_db))
                fav_l = [i[0] for i in cur.fetchall()]
                if bool(fav_l) is False:
                    raise ValueError
                for fav in fav_l:
                    cur.execute("SELECT name, lastname, vk_id FROM Ident WHERE id_db = '%s';" % (fav))
                    f_i = cur.fetchone()
                    yield {'name': f_i[0], 'lastname': f_i[1], 'url': fav_url+f_i[2], 'photo_iter':self.get_top3_photo(f_i[2])}
                conn.close()
            except ValueError:
                logger.warning('У пользователя никого нет в листе избранных')
                raise ValueError('Ошибка! У пользователя никого нет в листе избранных')
    def add_top3_photo(self):
        param_dict_photo['owner_id'] = f'{self.vk_id}'
        response = VK_SESSION.method(method='photos.get', values=param_dict_photo)
        photo_count = response['count']
        photo_list = sorted(response['items'], key=lambda x: x['likes']['count'], reverse=True)[:3]
        photo_dict = {f'link_photo{i}':f'photo{j["owner_id"]}_{j["id"]}' for i, j in enumerate(photo_list, start=1)}
        photo_dict_for_db = {i: j for i, j in zip_longest(photo_dict_lecal, photo_dict.values())}
        conn = psycopg2.connect(database=DataBase._database, user=DataBase._user, password=DataBase._password)
        try:
            with conn.cursor() as cur:
                cur.execute("""
                        INSERT INTO photo_top3(id_db, link_photo1, link_photo2, link_photo3)
                        VALUES (%s, %s, %s, %s) RETURNING link_photo1, link_photo2, link_photo3;
                        """, (self.id_db, photo_dict_for_db['link_photo1'], photo_dict_for_db['link_photo2'], photo_dict_for_db['link_photo3']))
                conn.commit()
                res_tup = tuple(cur.fetchone())
                res_iter = filter(lambda x: x != None, res_tup)
                conn.close()
                logger.info(f"{len(photo_dict)} фото с наибольшим кол-вом лайков добавлено пользавателю с vk_id-({self.vk_id}), всего фото на странице пользователя - {photo_count}")
                return res_iter
        except psycopg2.errors.UniqueViolation:
            pass
    def get_top3_photo(self, vk_id:str):
        conn = psycopg2.connect(database=DataBase._database, user=DataBase._user, password=DataBase._password)
        with conn.cursor() as cur:
            cur.execute("""SELECT link_photo1, link_photo2, link_photo3 FROM photo_top3 ph
                           LEFT JOIN ident a ON ph.id_db = a.id_db
                           WHERE vk_id = '%s';""" % (vk_id))
            response = cur.fetchone()
        conn.close()
        return filter(lambda x: x != None, response)
    def get_recommend(self):
        url = f'https://vk.com/id'
        conn = psycopg2.connect(database=DataBase._database, user=DataBase._user, password=DataBase._password)
        gender_reverse = 'Жен.' if self._user_info['gender'] == 'Муж.' else 'Муж.'
        age = self._user_info['age']
        age_interval = (age - 5, age + 5)
        city = self._user_info['city']
        with conn.cursor() as cur:
            cur.execute("""SELECT vk_id, name, lastname, age, link_photo1, link_photo2, link_photo3 FROM Ident
                           JOIN photo_top3 ph ON Ident.id_db = ph.id_db
                           WHERE age BETWEEN %s AND %s AND gender = '%s' AND city = '%s'""" % (age_interval[0], age_interval[1], 
                                                                                           gender_reverse, city))
            rec_l = cur.fetchall()
            conn.close()
            try:
                if bool(rec_l) is False:
                    raise ValueError
                for rec in rec_l:
                    photo_iter = filter(lambda x: x != None, (rec[4], rec[5], rec[6]))
                    yield {'vk_id':rec[0], 'name': rec[1], 'lastname': rec[2], 'age': rec[3], 'url': url + rec[0], 'city': city, 'photo_iter': photo_iter}
            except ValueError:
                raise ValueError('Данному пользователю из базы не найдено рекомендаций')
    @classmethod
    def vk_id_check(self, vk_id:str)->bool:
        conn = psycopg2.connect(database=DataBase._database, user=DataBase._user, password=DataBase._password)
        with conn.cursor() as cur:
            cur.execute("""SELECT vk_id FROM Ident
                            WHERE vk_id = '%s'""" % (vk_id))
            bol = cur.fetchall()
            conn.close()
        if bool(bol) is False:
            return False
        else:
            return True
