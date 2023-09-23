import json

from django.core.management import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка из csv файла'

    def handle(self, *args, **kwargs):
        if Ingredient.objects.exists():
            print('В базе уже есть ингредиент.')
            return
        try:
            with open(
                './data/ingredients.json',
                'r',
                encoding='utf-8'
            ) as file:
                jsondata = json.load(file)
                for line in jsondata:
                    if not Ingredient.objects.filter(
                       name=line['name'],
                       measurement_unit=line['measurement_unit']).exists():
                        Ingredient.objects.create(
                            name=line['name'],
                            measurement_unit=line['measurement_unit']
                        )
        except ValueError as error:
            print(f"A {type(error).__name__} has occurred.")
        else:
            print('Загрузка ингредиентов завершена')
