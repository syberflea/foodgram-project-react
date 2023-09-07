from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import UniqueConstraint
User = get_user_model()


class Tag(models.Model):
    '''Теги'''
    name = models.CharField(
        'Название',
        max_length=200,
        help_text=_('example: Завтрак.')
    )
    color = models.CharField(
        'Цвет в HEX',
        max_length=7,
        blank=True,
        null=True,
        help_text=_('example: #E26C2D')
    )
    slug = models.SlugField(
        '''Уникальный слаг''',
        max_length=200
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    '''Список ингредиентов с возможностью поиска по имени.'''
    name = models.CharField(
        '''Ингридиент''',
        max_length=200
    )
    measurement_unit = models.CharField(
        '''Единица измерения''',
        max_length=200
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    '''Список рецептов.'''
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Список тегов'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipies',
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        related_name='recipes',
        verbose_name='Список ингредиентов'
    )
    is_favorited = models.BooleanField(
        default=False,
        verbose_name='Находится ли в избранном'
    )
    is_in_shopping_cart = models.BooleanField(
        default=False,
        verbose_name='Находится ли в корзине'
    )
    name = models.CharField(
        'Название',
        max_length=200
    )
    image = models.ImageField(
        'Ссылка на картинку на сайте',
        upload_to='images/',
        null=True,
        blank=True
    )
    text = models.TextField(
        max_length=256,
        verbose_name='Описание'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления (в минутах)',
        default=1,
        validators=[
            MinValueValidator(
                1,
                message='Минимальное время готовки 1 мин.'
            ),
        ]
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    '''Модель для связи рецептов с ингредиентами.'''
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='elements',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='elements',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество (в граммах)',
        default=1,
        validators=[
            MinValueValidator(
                1,
                message='Минимальное количество 1 гр'
            ),
        ]
    )

    def __str__(self):
        return f"{self.recipe.name} {self.ingredient.name} {self.amount}"

    class Meta:
        verbose_name = 'Ингредиенты и Рецепты'
        verbose_name_plural = 'Ингредиенты и Рецепты'
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name="unique_ingredient_in_recipe"
            )
        ]


class Favorite(models.Model):
    '''Избранный рецепт'''
    user = models.ForeignKey(
        User,
        related_name='favorites',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorites',
        on_delete=models.CASCADE,
        verbose_name='рецепт'
    )

    class Meta:
        verbose_name = 'Рецепт избранный'
        verbose_name_plural = 'Рецепты избранные'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name="unique_favorite"
            )
        ]

        def __str__(self):
            return f"{self.user.name} likes {self.recipe.name}"


class ShopingCart(models.Model):
    '''Список покупок'''
    user = models.ForeignKey(
        User,
        related_name='shopingcarts',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name="shopingcarts",
        on_delete=models.CASCADE,
        verbose_name='рецепт'
    )

    class Meta:
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзине'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name="unique_shopingcart"
            )
        ]

    def __str__(self):
        return f"{self.user.name} buys {self.recipe.name}"
