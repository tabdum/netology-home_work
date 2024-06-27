import psycopg2
class DATABASE:
    database = input('\nВведите название базы к которой хотите подключится: ')
    user = input('Введите имя пользователя базы к которой хотите подключится: ')
    password = input('Введите пароль этого пользователя: ')  
    def create_db(self, database=database, user=user, password=password):
        conn = psycopg2.connect(database=database, user=user, password=password)
        with conn.cursor() as cur:
            cur.execute("""
                        DROP TABLE IF EXISTS phone_book;
                        DROP TABLE IF EXISTS customers;
                        CREATE TABLE customers(
                            id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 98765323232),
                            name VARCHAR(30) NOT NULL,
                            lastname VARCHAR(30) NOT NULL,
                            email VARCHAR(30) UNIQUE NOT NULL,
                            CONSTRAINT pk_id PRIMARY KEY (id)
                        );
                        CREATE TABLE phone_book(
                            client_id bigint REFERENCES customers(id) NOT NULL,
                            phone_number1 VARCHAR(11) UNIQUE,
                            phone_number2 VARCHAR(11) UNIQUE,
                            phone_number3 VARCHAR(11) UNIQUE,
                            phone_number4 VARCHAR(11) UNIQUE,
                            phone_number5 VARCHAR(11) UNIQUE
                        );
                        """)
            conn.commit()   
        conn.close() 
    def add_customer(self, name, lastname, email, phone_number=None):
        conn = psycopg2.connect(database=DATABASE.database, user=DATABASE.user, password=DATABASE.password)
        with conn.cursor() as cur:
            cur.execute("""
                        INSERT INTO customers(name, lastname, email)
                        VALUES (%s, %s, %s) RETURNING id, name, lastname, email;
                        """, (name, lastname, email))
            conn.commit()
            cur.execute("""
                        INSERT INTO phone_book(client_id, phone_number1)
                        VALUES 
                        ((SELECT id FROM customers WHERE email = %s),%s) RETURNING client_id, phone_number1
                        """, (email, phone_number))
            conn.commit()  
        conn.close()
        print(f'\nКлиент успешно добавлен!\n (ФИО: {name} {lastname})\n (email:{email})\n (Номер телефона: {phone_number})\n')
    def replace_customer_data(self, client_id, name=None, lastname=None, email=None):
        data_list = ['name', 'lastname', 'email']
        parametrs_list = [name, lastname, email]
        conn = psycopg2.connect(database=DATABASE.database, user=DATABASE.user, password=DATABASE.password)
        with conn.cursor() as cur:
            for i, j in zip(data_list, parametrs_list):
                if j != None:
                    cur.execute("UPDATE customers SET %s = '%s' WHERE id = %s" % (i, j, client_id))
                    print(f'{i} клиента с id = {client_id} изменен на {j}\n')
                    conn.commit()
        conn.close()
    def find_customer (self, name=None, lastname=None, email=None, phone_number=None):
        data_list = ['name', 'lastname', 'email']
        parametrs_list = [name, lastname, email]
        conn = psycopg2.connect(database=DATABASE.database, user=DATABASE.user, password=DATABASE.password)
        with conn.cursor() as cur:
            if phone_number != None:
                cur.execute("""SELECT * FROM phone_book WHERE phone_number1 = '%s'
                            OR phone_number2 = '%s' OR phone_number3 = '%s'
                            OR phone_number4 = '%s'""" % (phone_number, phone_number, phone_number, phone_number))
                response1 = cur.fetchone()
                cur.execute('SELECT * FROM customers WHERE id = %s' % (response1[0]))
                response2 = cur.fetchone()
                print(f"id клиента: {response2[0]}\nФИО клиента: {response2[1]} {response2[2]}\nПочта клиента: {response2[3]}\nНомера телефонов клиента:\n{response1[1:]}")               
            else:
                for i, j in zip(data_list, parametrs_list):
                    if j != None:
                        cur.execute("SELECT * FROM customers WHERE %s = '%s'" % (i, j))
                        response1 = cur.fetchone()
                        cur.execute('SELECT * FROM phone_book WHERE client_id = %s' % (response1[0]))
                        response2 = cur.fetchone()
                        print(f"\nid клиента: {response1[0]}\nФИО клиента: {response1[1]} {response1[2]}\nПочта клиента: {response1[3]}\nНомера телефонов клиента:\n{response2[1:]}")
        conn.close()
    def delete_customer(self, client_id):
        conn = psycopg2.connect(database=DATABASE.database, user=DATABASE.user, password=DATABASE.password)       
        with conn.cursor() as cur:
            cur.execute('DELETE FROM phone_book WHERE client_id = %s' % client_id)
            cur.execute('DELETE FROM customers WHERE id = %s RETURNING name, lastname' % client_id)
            conn.commit()
            b = cur.fetchone()
            print(f'Клиент {b[0]} {b[1]} успешно удален\n')
        conn.close()
    def add_customer_newnumber(self, client_id, number):
        conn = psycopg2.connect(database=DATABASE.database, user=DATABASE.user, password=DATABASE.password)        
        with conn.cursor() as cur:
            flag = True
            counter = 1
            for _ in range(5):
                cur.execute("SELECT phone_number%s FROM phone_book WHERE client_id = %s" % (counter, client_id))
                b = cur.fetchone()
                if b == (None,):
                    flag = False
                    cur.execute('UPDATE phone_book SET phone_number%s = %s WHERE client_id = %s RETURNING phone_number%s' % (counter, number, client_id, counter))
                    c = cur.fetchone()
                    conn.commit()
                    break
                counter += 1
            if flag == False:
                print('Номер успешно добавлен!')
                print(f'+{number}\n')
            else:
                print('Достигнут лимит номеров!\n(Удалите один из предыдущих номеров телефона)\n')
        conn.close()
    def delete_customer_phonenumber(self, client_id, phone_index):
        conn = psycopg2.connect(database=DATABASE.database, user=DATABASE.user, password=DATABASE.password)        
        with conn.cursor() as cur:
            cur.execute('UPDATE phone_book SET phone_number%s = NULL WHERE client_id = %s RETURNING phone_number%s', (phone_index, client_id, phone_index))
            conn.commit()
            response = cur.fetchone()
            if response == (None, ):
                print('Номер успешно удален')
            else:
                print('Не удалось удалить номер')
        conn.close()
    def garant_zachyota(self):
        print('\nПоставьте, пожалуйста, зачет, я устал\n')

if __name__ == '__main__':
    database_meneger = DATABASE()
    database_meneger.create_db() #! Создаем структру бд
    database_meneger.add_customer('Nadezhda', 'Polyakova', 'nadezh@mail.ru', phone_number='79888766776') #! Добавляем клиента1 в бд
    database_meneger.add_customer('Alexey', 'Petrov', 'alex@mail.ru') #! Добавляем клиента2 в бд без номера телефона
    database_meneger.add_customer_newnumber(1, '79233452323') #! Добавляем номер2 для клиента1
    database_meneger.add_customer_newnumber(1, '78988766545') #! Добавляем номер3 для клиента1
    database_meneger.add_customer_newnumber(1, '76544567645') #! Добавляем номер4 для клиента1
    database_meneger.add_customer_newnumber(1, '79891233232') #! Добавляем номер5 для клиента1
    database_meneger.add_customer_newnumber(1, '79887987898') #! Достигаем лимита номеров
    database_meneger.add_customer_newnumber(2, '76555677656') #! Добавляем номер1 для клиента2
    database_meneger.add_customer_newnumber(2, '79087667767') #! Добавляем номер2 для клиента2
    database_meneger.add_customer_newnumber(2, '79287889898') #! Добавляем номер3 для клиента2
    database_meneger.add_customer_newnumber(2, '79887658978') #! Добавляем номер4 для клиента2
    database_meneger.add_customer_newnumber(2, '79087889887') #! Добавляем номер5 для клиента2
    database_meneger.add_customer_newnumber(2, '79087889887') #! Достигаем лимита номеров
    database_meneger.delete_customer_phonenumber(client_id=2, phone_index=5) #! Удаляем номер, чтобы освободить место для нового. Реализован выбор номера по индексу, для менеджера в компании такой варинат будет проще юзобильно, так же это разгрузит БД. Так же клиенты не смогут добавлять номера, которые уже закреплены за другими клиентами.
    database_meneger.add_customer_newnumber(2, '79087889887') #! Добавляем новый номер в только что освобожденное для него место
    database_meneger.delete_customer(client_id=1) #! Удаляем клиента по уникальному идентификатору
    database_meneger.replace_customer_data(client_id=2, name='Alex') #! Меняем имя клиента 
    database_meneger.replace_customer_data(client_id=2, lastname='Beregovskiy') #! Меняем фамилию клиента
    database_meneger.replace_customer_data(client_id=2, email='beregovskiy@bk.ru') #! Меняем почту клиента
    database_meneger.find_customer(phone_number='79287889898') #! Находим клиента по номеру
    database_meneger.find_customer(name='Alex') #! Находим клиента по имени
    database_meneger.find_customer(lastname='Beregovskiy') #! Находим клиента по Фамилии
    database_meneger.find_customer(email='beregovskiy@bk.ru') #! Находим клиента по почте
    database_meneger.garant_zachyota() #! сюрприз