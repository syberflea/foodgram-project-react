from django.core.management import BaseCommand
from recipes.models import Tag


class Command(BaseCommand):
    help = 'Создание шаблонных тегов в базе данных.'

    def handle(self, *args, **kwargs):
        data = [
            {'name': 'Завтрак', 'color': '#E26C2D', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#006b1b', 'slug': 'dinner'},
            {'name': 'Ужин', 'color': '#61affe', 'slug': 'supper'},
            {'name': 'Первое', 'color': '#287233', 'slug': 'first'},
            {'name': 'Второе', 'color': '#ffa500', 'slug': 'second'},
            {'name': 'Компот', 'color': '#f5f5dc', 'slug': 'kompot'},
        ]
        try:
            Tag.objects.bulk_create(Tag(**tag) for tag in data)
        except ValueError as error:
            print(f"A {type(error).__name__} has occurred.")
        else:
            print('Создание тегов завершено')
