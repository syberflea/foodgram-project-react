
from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (
    Favorite, Ingredient, IngredientInRecipe, Recipe, ShopingCart, Tag,
)
from rest_framework import serializers, status
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)
        read_only_fields = ('id', 'name', 'measurement_unit',)


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    ingredients = IngredientInRecipeSerializer(
        many=True,
        read_only=True,
        source='ingredientrecipes'
    )

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
        return user.shopingcarts.filter(recipe=obj).exists()

    def get_ingredients(self, obj):
        ingredients = IngredientInRecipeSerializer.objects.filter(recipe=obj)
        return IngredientInRecipeSerializer(ingredients, many=True).data

    def validate(self, data):
        ingredients = self.initial_data['ingredients']
        ingredients_list = []
        if not ingredients:
            raise serializers.ValidationError(
                'Необходимо указать как минимум один ингредиент'
            )
        for item in ingredients:
            if int(item['amount']) < 1:
                raise serializers.ValidationError(
                    'Минимальное количество ингредиента меньше 1'
                )
            ingredient = get_object_or_404(
                Ingredient, id=item['id']
            )
            if ingredient in ingredients_list:
                raise serializers.ValidationError(
                    'Указано несколько одинаковых ингредиентов'
                )
            ingredients_list.append(ingredient)
        data['ingredients'] = ingredients
        return data

    def validate_tags(self, data):
        tags = self.initial_data['tags']
        if not tags:
            raise serializers.ValidationError(
                'Необходимо указать как минимум один тег'
            )
        lst = []
        for tag in tags:
            lst.append(tag)
        data['tags'] = tags
        return data

    def _add_elements_to_recipe(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredientInRecipe.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient['amount'],
            )

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        tags = self.initial_data.get('tags')
        recipe.tags.set(tags)
        self._add_elements_to_recipe(ingredients, recipe)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.tags.clear()
        tags = self.initial_data.get('tags')
        instance.tags.set(tags)
        IngredientInRecipe.objects.filter(recipe=instance).all().delete()
        ingredients = validated_data.pop('ingredients')
        self._add_elements_to_recipe(ingredients, instance)
        return super().update(instance, validated_data)


class FavoriteSerializer(RecipeSerializer):
    name = serializers.ReadOnlyField()
    cooking_time = serializers.ReadOnlyField()

    class Meta(RecipeSerializer.Meta):
        fields = ('id', 'name', 'image', 'cooking_time')

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
        fields = ('id', 'name', 'image', 'cooking_time')

    def validate(self, data):
        recipe = self.instance
        user = self.context.get('request').user
        if ShopingCart.objects.filter(recipe=recipe, user=user).exists():
            raise serializers.ValidationError(
                detail='Рецепт уже добавлен в корзину',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data
