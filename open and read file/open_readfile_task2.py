from pprint import pprint
with open('recipes.txt', encoding='utf-8') as file:
    cook_book = {}
    def append_ingridient(keys, range_long):
        ing_list = []
        b = file.readline()
        b_none = file.readline()
        for i in range(range_long):
            dict_book_omlet = {}
            b = file.readline().strip()
            b = b.replace('|', '')
            b = b.split()
            dict_book_omlet["ingridents_name"] = b[0]
            dict_book_omlet["quantity"] = b[1]
            dict_book_omlet["measure"] = b[2]
            ing_list.append(dict_book_omlet)
        file.readline()
        # pprint(ing_list)
        cook_book[keys] = ing_list
        return cook_book

    append_ingridient('Омлет', 3)
    append_ingridient('Утка по-пекински', 4)
    append_ingridient('Запеченный картофель', 3)
    append_ingridient('Фахитос', 5)

dishes_list = ["Запеченный картофель", 'Омлет']
def get_shop_list_by_dishes(dishes, person_count):
    cook_book_copy = cook_book.copy()
    dishes_dict = {}
    for dish in dishes:
        b = cook_book_copy[dish]
        for i in b:
            i["quantity"] = str(int(i["quantity"]) * person_count)
        dishes_dict[dish] = cook_book_copy[dish]
    return dishes_dict

pprint(get_shop_list_by_dishes(dishes_list, 2), width=100)


