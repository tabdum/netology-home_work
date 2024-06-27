from re import sub, findall, search
import csv
def get_list_index(lst: list, index: int, value=None):
    if index > len(lst) - 1:
        return value
    return lst[index]
patern = r'\+?\d\D*(\d{3})\D*(\d{3})\D*(\d{2})\D*(\d{2})\D?(.*(доб\.).?(\d+).?)?'
with open("phonebook_raw.csv", encoding="utf-8", newline='') as f:
  rows = csv.DictReader(f, delimiter=",")
  contact_list = list(rows)
  contact_headers = rows.fieldnames
for index, row in enumerate(contact_list):
  b = f"{row['lastname']} {row['firstname']} {row['surname']}".split()
  contact_list[index]['lastname'] = get_list_index(b, 0)
  contact_list[index]['firstname'] = get_list_index(b, 1)
  contact_list[index]['surname'] = get_list_index(b, 2)
  if search(patern, row['phone']) is not None:
    if '' not in findall(patern, row['phone'])[0]:
      s = sub(patern, r'+7(\1)\2-\3-\4 \6\7', row['phone'])
      contact_list[index]['phone'] = s
    else:
      sn = sub(patern, r'+7(\1)\2-\3-\4', row['phone'])
      contact_list[index]['phone'] = sn
sor2 = sorted(contact_list, key=lambda x: f"{x['lastname']} {x['firstname']}")
res_lis = []
for index, person1 in enumerate(sor2):
  str1 = f"{person1['lastname']}{person1['firstname']}"
  for person2 in sor2[index+1:]:
    str2 = f"{person2['lastname']}{person2['firstname']}"
    if str1 == str2:
      res_lis.append([person1, person2])
      break
for i in res_lis:
  for j in i:
    for k in j:
      if j[k] in (None, ''):
        j[k] = i[1][k]
res_lis2 = []
for i in res_lis:
  for j in i:
    res_lis2.append(j)
    break
l_f = [i['lastname'] + i['firstname'] for i in res_lis2]
f = list(filter(lambda x: x['lastname'] + x['firstname'] not in l_f, contact_list))
f.extend(res_lis2)
finish = []
for i in f:
  finish.append(list(i.values()))
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerow(contact_headers)
  datawriter.writerows(finish)
  