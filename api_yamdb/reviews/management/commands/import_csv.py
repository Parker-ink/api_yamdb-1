import contextlib
import csv
import os

from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '''Загрузка тестовой информации из csv-файла в базу данных.
    Вся существующая информация будет удалена из базы данных.'''

    # имя файла с данными, приложение, модель
    DATA = (
        ('users.csv', 'users', 'User'),
        ('category.csv', 'reviews', 'Category'),
        ('genre.csv', 'reviews', 'Genre'),
        ('titles.csv', 'reviews', 'Title'),
        ('review.csv', 'reviews', 'Review'),
        ('comments.csv', 'reviews', 'Comment'),
        ('genre_title.csv', 'reviews', 'GenreTitle'),
    )

    def handle(self, *args, **kwargs):
        message = 'Данные добавлены!'

        # Если БД существует, очищаем её таблицы от данных
        with contextlib.suppress(ValueError):
            call_command('flush', '--no-input')

        # Выполняем миграции
        call_command('migrate')

        # Импорт данных из файлов в БД
        for fixture, app, model in self.DATA:

            # Импортрируем модель
            try:
                current_model = apps.get_model(app, model)
            except LookupError:
                message = (f'Данные не добавлены!!! '
                           f'Ошибка в наименованиях приложений и моделей: '
                           f'{app}, {model}')
                break

            # Получаем полный путь до файла с данными
            path_to_file = os.path.join(
                settings.BASE_DIR, 'static', 'data', fixture
            )
            if not os.path.exists(path_to_file):
                message = (f'Данные не добавлены!!! '
                           f'Такой файл не существует: {path_to_file}')
                break

            with open(path_to_file, newline='') as csvfile:

                # Получаем данные из csv файла
                reader = csv.DictReader(csvfile)

                # Формируем список данных
                bulk_data = [current_model(**row) for row in reader]

                # Сохраняем данные в БД
                current_model.objects.bulk_create(bulk_data)

        self.stdout.write(message)
