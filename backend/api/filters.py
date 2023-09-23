from django_filters import rest_framework as filters
from django_filters.widgets import BooleanWidget
from recipes.models import Recipe, Tag
from rest_framework.filters import SearchFilter


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    author = filters.CharFilter()
    is_in_shopping_cart = filters.BooleanFilter(
        widget=BooleanWidget(),
        label='В корзине'
    )
    is_favorited = filters.BooleanFilter(
        widget=BooleanWidget(),
        label='В избранном'
    )

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited']
