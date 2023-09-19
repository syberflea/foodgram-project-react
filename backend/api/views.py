from recipes.models import Favorite, Ingredient, Recipe, Tag
from rest_framework import viewsets

from .pagination import CustomPagination
from .permissions import AuthorOrReadOnlyPermission
from .serializers import (
    FavoriteSerializer, IngredientSerializer, RecipeSerializer, TagSerializer,
)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
    permission_classes = (AuthorOrReadOnlyPermission, )
