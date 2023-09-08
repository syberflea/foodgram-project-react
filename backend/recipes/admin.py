from django.contrib import admin

from .models import (
    Favorite, Ingredient, IngredientInRecipe, Recipe, ShopingCart, Tag,
)
from import_export.admin import ImportExportModelAdmin


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
    )
    search_fields = ('name', 'author')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )


class IngredientAdmin(ImportExportModelAdmin):
    pass


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
