from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from recipes.models import Favorite, Ingredient, Recipe, Tag
from rest_framework import viewsets
from users.models import User

from .serializers import (
    CustomUserSerializer, FavoriteSerializer, IngredientSerializer,
    RecipeSerializer, TagSerializer,
)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


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
