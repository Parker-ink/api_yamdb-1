import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import (
    Category, Comment, Genre, GenreTitle, Review, Title
)
from users.models import User


class Command(BaseCommand):
    help = u'''
    Загрузка информации из csv-файла в базу данных.
    Для импорта данных выполните команды в следующем порядке:
    1) python3 manage.py import_csv users
    2) python3 manage.py import_csv category
    3) python3 manage.py import_csv genre
    4) python3 manage.py import_csv titles
    5) python3 manage.py import_csv review
    6) python3 manage.py import_csv comments
    7) python3 manage.py import_csv genre_title
    '''

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name',
            type=str,
            help=u'Имя файла без расширения'
        )

    def handle(self, *args, **kwargs):
        file_name = f"{kwargs['file_name']}.csv"
        path_to_file = os.path.join(
            settings.BASE_DIR, 'static', 'data', file_name
        )
        with open(path_to_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:

                if file_name == 'users.csv':
                    User.objects.create(**row)

                elif file_name == 'category.csv':
                    Category.objects.create(**row)

                elif file_name == 'genre.csv':
                    Genre.objects.create(**row)

                elif file_name == 'titles.csv':
                    Title.objects.create(**row)

                elif file_name == 'review.csv':
                    Review.objects.create(**row)

                elif file_name == 'comments.csv':
                    Comment.objects.create(**row)

                elif file_name == 'genre_title.csv':
                    GenreTitle.objects.create(**row)

        self.stdout.write("Данные добавлены")
