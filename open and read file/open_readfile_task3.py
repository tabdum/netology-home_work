def line_counter(file_name):
    with open(file_name) as fp:
        count = 0
        for line in fp:
            count += 1
    return f"\n\n{count}\n"
#
def lister(file_name):
    with open(file_name) as fs:
        file_1 = []
        for line in fs:
            file_1.append(line)
    return file_1

import os
directory = "/home/azamat/Desktop/py-homework-basic-files/2.4.files/sorted"
file_name = os.listdir(directory)
for i in range(len(file_name)):
    if file_name[i].endswith('txt') == False:
        file_name -= file_name[i]

file_dict = {}
for file in file_name:
    with open(file, encoding='utf-8') as files:
        b = []
        for count, line in enumerate(files):
            b.append(line)
            file_dict[file] = [count + 1] + b
sorted_file = []

for d in file_dict:
    b = file_dict[d]
    b = b[0]
    sorted_file += [[b] + [d]]
sorted_file.sort()
sorted_files = []

for u in sorted_file:
    sorted_files.append(u[1])

for k in sorted_files:
    with open("complicte.txt", "a", encoding='utf-8') as fp:
        fp.writelines(lister(k))
        fp.write(line_counter(k))
