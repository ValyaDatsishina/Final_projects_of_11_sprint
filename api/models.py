from django.contrib.auth.base_user import BaseUserManager
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import UniqueConstraint


class CustomManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(email, password=password, **kwargs)
        user.role = 'admin'
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USER_ROLES = (
        ('admin', 'admin'),
        ('user', 'user'),
        ('moderator', 'moderator')
    )

    email = models.EmailField(unique=True)
    username = models.SlugField(unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    confirmation_code = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=50, choices=USER_ROLES, default='user', null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)


class Titles(models.Model):
    name = models.CharField(max_length=150)
    year = models.PositiveSmallIntegerField()
    description = models.TextField(max_length=300, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="titles",
                                 blank=True, null=True)
    genre = models.ManyToManyField(Genre)


class Review(models.Model):
    title_id = models.ForeignKey(Titles, on_delete=models.CASCADE, related_name="review")
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review")
    score = models.IntegerField()
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text


class Comments(models.Model):
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True, db_index=True)
