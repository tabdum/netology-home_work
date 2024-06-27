import types
import os, functools
from datetime import datetime
def logger(path):
    def loger(old_function):
        @functools.wraps(old_function)
        def new_function(*args, **kwargs):
            result = old_function
            date_time = datetime.now()
            arguments = (*args, *kwargs.values())
            function_name = new_function.__name__
            for i in result(*args):
                yield i
                result_string = f'время: {date_time}, имя функции:{function_name}, aргумент: {arguments}, сгенерированный элемент:{i}\n'
                with open(path, 'a', encoding='utf-8') as file:
                    file.write(result_string)
        return new_function
    return loger

def test_2():
    path = 'gen.log'    
    @logger(path)
    def flat_generator(list_of_lists):
        for i in list_of_lists:
            for j in i:
                yield j
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]
    assert all(i != list for i in flat_generator(list_of_lists_1)) is True, 'Элементы не распакованы'
    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType), 'Функция не является генератом'
    assert os.path.exists(path), 'Файл не существует'
if __name__ == '__main__':
    test_2()

