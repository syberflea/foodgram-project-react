from django.contrib import admin

from .models import (
    Favorite, Ingredient, IngredientInRecipe, Recipe, ShopingCart, Tag,
)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
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
    pass


class FavoriteRecipeAdmin(admin.ModelAdmin):
    pass


class ShopingCartAdmin(admin.ModelAdmin):
    pass


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(IngredientInRecipe, IngredientInRecipeAdmin)
admin.site.register(Favorite, FavoriteRecipeAdmin)
admin.site.register(ShopingCart, ShopingCartAdmin)
