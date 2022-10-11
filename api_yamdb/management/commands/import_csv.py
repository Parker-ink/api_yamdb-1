import csv
import os

from django.conf import BASE_DIR
from django.core.management.base import BaseCommand

from reviews.models import (
    Category, Comment, Genre, Review, Title, User
)
from users.models import User


class Command(BaseCommand):
    help = u'Загрузка информации из csv-файла в базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name',
            type=str,
            help=u'Имя файла без расширения'
        )

    def handle(self, *args, **kwargs):
        file_name = f"{kwargs['file_name']}.csv"
        path_to_file = os.path.join(BASE_DIR, 'static/data/', file_name)
        with open(path_to_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if file_name == 'users.csv':
                    User.objects.create(**row)
                elif file_name == 'titles.csv':
                    Title.objects.create(**row)
                elif file_name == 'review.csv':
                    Review.objects.create(**row)
                elif file_name == 'genre.csv':
                    Genre.objects.create(**row)
                elif file_name == 'comments.csv':
                    Comment.objects.create(**row)
                elif file_name == 'category.csv':
                    Category.objects.create(**row)
        self.stdout.write("Данные добавлены")
