import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from recipes.models import (
    Favorite, Ingredient, IngredientInRecipe, Recipe, ShopingCart, Tag,
)
from rest_framework import serializers, status
from users.serializers import CustomUserSerializer


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name=f'temp.{ext}')

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('pk', 'name', 'measurement_unit', 'amount',)


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = IngredientInRecipeSerializer(many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shoppingcarts.filter(recipe=obj).exists()

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                'Необходимо указать как минимум один ингредиент'
            )
        ingredients_id_list = []
        for item in value:
            if item['amount'] == 0:
                raise serializers.ValidationError(
                    'Количество ингредиента не может быть равным нулю'
                )
            ingredient_id = item['ingredient']['id']
            if ingredient_id in ingredients_id_list:
                raise serializers.ValidationError(
                    'Указано несколько одинаковых ингредиентов'
                )
            ingredients_id_list.append(ingredient_id)
        return value

    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError(
                'Необходимо указать как минимум один тег'
            )
        return value

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            ingredient_amount = ingredient.pop("amount")
            ingredient_obj = get_object_or_404(
                Ingredient, id=ingredient['ingredient']['id']
            )
            IngredientInRecipe.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient_obj,
                amount=ingredient_amount
            )
            recipe.ingredients.add(ingredient_obj)
        return recipe

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        return self.create_ingredients(ingredients, recipe)

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_ingredients(ingredients, recipe=instance)
        return instance


class FavoriteSerializer(RecipeSerializer):
    name = serializers.ReadOnlyField()
    cooking_time = serializers.ReadOnlyField()

    class Meta(RecipeSerializer.Meta):
        fields = ("id", "name", "image", "cooking_time")

    def validate(self, data):
        recipe = self.instance
        user = self.context.get('request').user
        if Favorite.objects.filter(recipe=recipe, user=user).exists():
            raise serializers.ValidationError(
                detail='Рецепт уже добавлен в избранное',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data


class ShoppingCartSerializer(RecipeSerializer):
    name = serializers.ReadOnlyField()
    cooking_time = serializers.ReadOnlyField()

    class Meta(RecipeSerializer.Meta):
        fields = ("id", "name", "image", "cooking_time")

    def validate(self, data):
        recipe = self.instance
        user = self.context.get('request').user
        if ShopingCart.objects.filter(recipe=recipe, user=user).exists():
            raise serializers.ValidationError(
                detail='Рецепт уже добавлен в корзину',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data
