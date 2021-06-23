from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class SuperUser(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, photo='', phone='', about_me='', password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'

    class Gender(models.TextChoices):
        men = 'M', _('Мужской')
        women = 'Ж', _('Женский')

    email = models.EmailField(verbose_name='Почта', max_length=120, unique=True)
    username = models.CharField(verbose_name='Username', max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name='Дата регистрации', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Последний вход', auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    first_name = models.CharField(verbose_name='Имя', max_length=30)
    last_name = models.CharField(verbose_name='Фамилия', max_length=60)
    patronymic = models.CharField(verbose_name='Отчество', max_length=40, default='', blank=True)

    phone = PhoneNumberField(verbose_name='Телефон', max_length=15, default='', blank=True)
    photo = models.ImageField(verbose_name='Аватарка', upload_to='static/user/avatar',
                              default='static/user/avatar/default_avatar.png', blank=True)
    gender = models.CharField(verbose_name='Пол', max_length=1, choices=Gender.choices, blank=True)

    mail_notify = models.BooleanField(verbose_name='Уведомления по почте', default=True)
    telegram_notify = models.BooleanField(verbose_name='Уведомления в телеграмме', default=False)
    vk_notify = models.BooleanField(verbose_name='Уведомления в вк', default=False)
    telegram_id = models.BigIntegerField(verbose_name='telegram id', default=0, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', ]

    objects = SuperUser()

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_active
