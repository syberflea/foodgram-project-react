from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from recipes.models import Favorite, Ingredient, Recipe, Tag
from rest_framework import serializers

User = get_user_model()


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model: Ingredient
        fields = '__all__'


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name') 
