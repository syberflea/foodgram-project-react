from django.contrib import admin
from users.models import User

from .models import Ingredient, Recipe, Tag, IngredientInRecipe


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'tags',
        'author',
        'ingredients',
        'is_favorited',
        'is_in_shopping_cart',
        'name',
        'image',
        'text',
        'cooking_time',
    )
    search_fields = ('name', 'author')
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )


class IngredientInRecipeAdmin(admin.ModelAdmin):
    '''Админка для связуещего класса IngredientInRecipeAdmin'''


admin.site.register(User)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(IngredientInRecipe, IngredientInRecipeAdmin)
