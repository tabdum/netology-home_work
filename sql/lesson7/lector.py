# import sqlalchemy
# DSN = 'postgresql://postgres:25458914@localhost:5432/lesson7'
# engine = sqlalchemy.create_engine(DSN)
# Session = sqlalchemy.sessionmaker(bind=engine)
# session = Session()
# session.close()
# print('how are you')
# def filter(function, items):
#     result = []
#     for item in items:
#         if function(item):        
#             result.append(item)  # добавляем элемент item если функция function вернула значение True
#     return result

# def is_odd(num):
#     return num % 2
# numbers = list(range(15))
# print(is_odd(3))

# # odd_numbers = filter(is_odd, numbers)
# # print(odd_numbers)
