from django.db import models
from colorfield.fields import ColorField
from django.core.validators import MinValueValidator

from users.models import User

MESSAGE_COOKING_TIME = 'Время приготовления не может быть меньше минуты.'
MESSAGE_AMOUNT = 'Количество должно быть равно хотя бы одному'


class Ingredient(models.Model):
    """ Ингридиенты для рецепта. """
    name = models.CharField(
        'Название ингридиента',
        max_length=200,
    )
    measurement_unit = models.CharField(
        'Еденицы измерения',
        max_length=200,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self) -> str:
        """Строковое представление объекта модели."""
        return f'{self.name} - {self.measurement_unit}'


class Tag(models.Model):
    """ Теги для рецептов."""
    name = models.CharField(
        'Тэг',
        max_length=200,
        unique=True,
    )
    color = ColorField(default='#FF0000', format='hexa')
    slug = models.SlugField(
        'Уникальный адрес',
        max_length=200,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self) -> str:
        """Строковое представление объекта модели."""
        return self.name


class Recipe(models.Model):
    """ Рецепты. """
    name = models.CharField(
        'Название рецепта',
        max_length=200
    )
    image = models.ImageField(
        'Изображение рецепта',
        upload_to='recipes/images',
        null=True,
        default=None
    )
    text = models.TextField(
        'Описание',
        max_length=1000,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=(MinValueValidator(
            1, message=MESSAGE_COOKING_TIME),)
    )
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)
        default_related_name = 'recipes'

    def __str__(self) -> str:
        """Строковое представление объекта модели."""
        return self.name


class IngredientRecipe(models.Model):
    """ Количество ингридиентов в рецепте блюда.
        Вспомогательная модель.
    Связывает модели Recipe и Ingredient.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=(MinValueValidator(
            1, message=MESSAGE_AMOUNT),)
    )

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
        default_related_name = 'amount_ingredients'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient',),
                name='unique_ingredient'
            ),
        )

    def __str__(self) -> str:
        """Строковое представление объекта модели."""
        return f'{self.amount} {self.ingredient}'


class Favorite(models.Model):
    """ Избранные рецепты.

    Связывает модели Recipe и  User.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    date_added = models.DateTimeField(
        verbose_name="Дата добавления",
        auto_now_add=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        default_related_name = 'favorites'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='%(app_label)s_%(class)s_unique'
            ),
        )

    def __str__(self) -> str:
        """Строковое представление объекта модели."""
        return f'{self.user}  {self.recipe}'


class ShoppingCart(models.Model):
    """ Список покупок. """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        default_related_name = 'cart'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_shopping_cart'
            ),
        )

    def __str__(self):
        return f'{self.user} :: {self.recipe}'


class Subscription(models.Model):
    """ Подписки пользователей друг на друга. """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор'
    )
    date_added = models.DateTimeField(
        'Дата создания подписки',
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author',),
                name='unique_subscriber'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='you_can_not_subscribe_to_yourself'
            ),
        )

    def __str__(self) -> str:
        """Строковое представление объекта модели."""
        return f'{self.user} подписан на {self.author}'
