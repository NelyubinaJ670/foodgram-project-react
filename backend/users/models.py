from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import validate_username


class User(AbstractUser):
    """Переопределяем модель User"""

    username = models.CharField(
        'Пользователь',
        max_length=150,
        unique=True,
        validators=[validate_username]
    )
    email = models.EmailField(
        'Эл.почта',
        unique=True,
        max_length=254
    )
    first_name = models.CharField(
        'Имя',
        max_length=150
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self) -> str:
        """Строковое представление объекта модели."""
        return self.username


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
