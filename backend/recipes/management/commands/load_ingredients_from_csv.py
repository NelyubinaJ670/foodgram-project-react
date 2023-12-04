import csv

import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient

logging.basicConfig(
    level=logging.DEBUG,
    filename='program.log',
    filemode='w',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)


class Command(BaseCommand):
    """
    Для запуска команды создайте и примените миграции
    и примените команду python manage.py load_ingredients_from_csv
    Базу нужно заполнить на чистую и только один раз.
    Чтобы повторно заполнить базу - удалите файл db.sqlite3
    и примените миграции, иначе будет ошибка.
    """
    help = 'Заполняет таблицу с ингридиентами'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Начат импорт данных'))
        try:
            with open(
                f'{settings.BASE_DIR}/data/ingredients.csv',
                newline='',
                encoding='utf-8'
            ) as csvfile:
                reader = csv.DictReader(csvfile)
                Ingredient.objects.bulk_create(
                    Ingredient(**row) for row in reader
                )
            self.stdout.write(
                self.style.SUCCESS(
                    'Ингридиенты успешно загруженны')
            )
        except Exception as error:
            logging.error(f'Ошибка при выполнении команды: {error}')
