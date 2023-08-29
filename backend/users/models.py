from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _
from users.validators import UsernameRegexValidator


class User(AbstractUser):
    '''Пользователь (В рецепте - автор рецепта)'''
    username_validator = UsernameRegexValidator()
    username = models.CharField(
        'Уникальный юзернейм',
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. '
            'Letters, digits and @/./+/-/_ only.'
        ),
        validators=[username_validator, ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия'
    )
    is_subscribed = models.BooleanField(
        default=False,
        verbose_name='Подписан ли текущий пользователь на этого'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username


class Follow(models.Model):
    '''Подписчики'''
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        constraints = [
            UniqueConstraint(
                fields=['user', 'following'],
                name='unique_following'
            )
        ]
