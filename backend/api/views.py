from django.contrib.auth import get_user_model
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import HttpResponse

from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from djoser.views import UserViewSet

from users.models import User
from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    ShoppingCart,
    Favorite,
    Subscription
)
from api.utils import create, delete
from api.filters import RecipeFilter
from api.permissions import OwnerOrReadOnly
from api.serializers import (
    TagSerializer,
    UserSerializer,
    IngredientSerializer,
    RecipeGetSerializer,
    RecipeSerializer,
    RecipeFavoriteSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer,
    SubscriptionReadSerializer,
    SubscriptionSerializer
)

User = get_user_model()


class TagViewSet(viewsets.ModelViewSet):
    """ Вьюсет для модели Tag """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    """ Вьюсет для модели Ingredient. """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        ingredients = self.request.query_params.get('name')
        if ingredients is not None:
            queryset = queryset.filter(name__istartswith=ingredients)
        return queryset


class RecipeViewSet(viewsets.ModelViewSet):
    """ Вывод для модели Recipe. """
    queryset = Recipe.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (OwnerOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        recipes = Recipe.objects.prefetch_related(
            'amount_ingredients__ingredient',
            'tags'
        ).all()
        return recipes

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_serializer_class(self):
        """ Метод вибирает сериализатор. """
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeGetSerializer
        return RecipeSerializer

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk):
        """Добавить или удалить рецепт в список "Избранное."""

        if request.method == 'POST':
            serializer = create(
                request,
                pk,
                FavoriteSerializer,
                RecipeFavoriteSerializer,
                Recipe
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        delete(request, pk, Recipe, Favorite)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk):
        """ Добавить или удалить ингредиенты рецепта в "Корзину покупок" """

        if request.method == 'POST':
            serializer = create(
                request,
                pk,
                ShoppingCartSerializer,
                RecipeFavoriteSerializer,
                Recipe
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        delete(request, pk, Recipe, ShoppingCart)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            permission_classes=(permissions.IsAuthenticated,))
    def download_shopping_cart(self, request):
        """ Скачать файл со списком покупок. """

        ingredient_lst = ShoppingCart.objects.filter(
            user=request.user
        ).values_list(
            'recipe_id__ingredients__name',
            'recipe_id__ingredients__measurement_unit',
            Sum('recipe_id__ingredients__amount_ingredients__amount'))

        shopping_list = ['Список покупок:']
        ingredient_lst = set(ingredient_lst)

        for ingredient in ingredient_lst:
            shopping_list.append('{} ({}) - {}'.format(*ingredient))

        response = HttpResponse('\n'.join(shopping_list),
                                content_type='text/plain')
        response['Content-Disposition'] = \
            'attachment; filename="shopping_list.txt"'
        return response


class CustomUserViewSet(UserViewSet):
    """ Вьюсет для модели User. """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
    )
    def subscribe(self, request, id):
        """ Метод создает/удаляет связь между пользователями. """
        if request.method == 'POST':
            serializer = create(
                request,
                id,
                SubscriptionSerializer,
                SubscriptionReadSerializer,
                User
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        delete(request, id, User, Subscription)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
    )
    def subscriptions(self, request):
        """ Список подписок у пользователя. """
        user = request.user
        authors = User.objects.filter(subscribing__user=user)

        paged_queryset = self.paginate_queryset(authors)
        serializer = SubscriptionReadSerializer(
            paged_queryset,
            context={'request': request},
            many=True
        )
        return self.get_paginated_response(serializer.data)