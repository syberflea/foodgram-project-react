from djoser.views import UserViewSet
from recipes.models import Favorite, Ingredient, Recipe, Tag
from rest_framework import viewsets
from users.models import User

from .pagination import CustomPagination
from .permissions import AuthorOrReadOnlyPermission
from .serializers import (
    CustomUserSerializer, FavoriteSerializer, IngredientSerializer,
    RecipeSerializer, TagSerializer, CustomUserCreateSerializer
)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return CustomUserCreateSerializer
        return CustomUserSerializer


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
