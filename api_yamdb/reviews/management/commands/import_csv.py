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
        with contextlib.suppress(ValueError):
            call_command('flush', interactive=False)
        call_command('migrate')
        for fixture, app, model in self.DATA:
            try:
                current_model = apps.get_model(app, model)
            except LookupError:
                message = (f'Данные не добавлены!!! '
                           f'Ошибка в наименованиях приложений и моделей: '
                           f'{app}, {model}')
                break
            path_to_file = os.path.join(
                settings.BASE_DIR, 'static', 'data', fixture
            )
            if not os.path.exists(path_to_file):
                message = (f'Данные не добавлены!!! '
                           f'Такой файл не существует: {path_to_file}')
                break
            with open(path_to_file, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                bulk_data = [current_model(**row) for row in reader]
                current_model.objects.bulk_create(bulk_data)
        self.stdout.write(message)
