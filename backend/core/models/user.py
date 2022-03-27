from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
from .bankAccounts import MockedBankAccount

from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.hashers import make_password

class CustomUserManager(UserManager):
    def _create_user(self, email, cpf, password, name, tel, **extra_fields):
        if not email:
            raise ValueError('The e-mail field is required')
        email = self.normalize_email(email)

        if not name:
            raise ValueError('User name is required')

        if not password:
            raise ValueError('Password is required')

        if not cpf:
            raise ValueError('CPF is required')
        user = User(email=email,name=name,cpf=cpf,tel=tel, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        user.accounts.set([])
        user.save(using=self._db)
        return user

    def create_user(self, email, cpf, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, cpf, password, **extra_fields)

    def create_superuser(self, email, cpf, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        assert extra_fields['is_staff']
        assert extra_fields['is_superuser']
        return self._create_user(email, cpf, password, **extra_fields)

class User(AbstractUser):
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=500)
    name = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, null=True)
    tel = models.CharField(max_length=15, blank=True, null=True)

    #O tratamento para esta lista de contas deve ser alterado a partir da implementação do sistema de CRUD de consentimento
    accounts = models.ManyToManyField(MockedBankAccount, blank=False, default=None, null=True)

    username = None

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','cpf']

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@host.local",
        # to:
        [reset_password_token.user.email]
    )