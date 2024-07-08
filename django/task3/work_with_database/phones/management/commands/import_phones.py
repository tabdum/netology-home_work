import csv
import os
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from phones.models import Phone
from pathlib import Path
from ...external_data.path_manage import file_path

target_list = os.listdir(str(file_path).replace('/path_manage.py', ''))
target_dir = str(file_path).replace('/path_manage.py', '')


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str)

    def handle(self, *args, **kwargs):
        try:
            with open(f"{target_dir}/{kwargs['file_name']}", 'r') as file:
                phones = list(csv.DictReader(file, delimiter=';'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Файл: {kwargs['file_name']} - не найден"))
        for phone in phones:
            slug = phone['name'].replace(' ', '-').lower()
            try:
                Phone.objects.create(name=phone['name'],
                                     price=phone['price'],
                                     image=phone['image'],
                                     release_date=phone['release_date'],
                                     lte_exists=phone['lte_exists'],
                                     slug=slug,
                                     )
                self.stdout.write(self.style.SUCCESS(f"Телефон: {phone['name']} успешно загружен в БД"))

            except Exception as err:
                self.stdout.write(self.style.ERROR(f"Телефон: {phone['name']} - не Загружен\n{err}"))


