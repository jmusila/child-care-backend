from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)


class UserManager(BaseUserManager):
    """
    Inheriting from BaseUserManager Class lets us use the django user
    We will therefore override the method create_user while creating our user
    """

    def create_user(self, username, email, password=None):
        """ Create and return a user with username, email and password"""
        if username is None:
            raise TypeError('Username is required.')

        if email is None:
            raise TypeError('Email is required.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, username, email, password):
        """ creates an admin user """
        if password is None:
            raise TypeError('Admin users must have a password')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    def get_by_natural_key(self, username):
        return self.get(username=username)


class User(AbstractBaseUser, PermissionsMixin):
    """ indexing fields in the db """
    username = models.CharField(db_index=True, max_length=255, unique=True)

    email = models.EmailField(db_index=True, unique=True)

    is_active = models.BooleanField(default=True)

    is_verified = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    email_notification = models.BooleanField(default=True)

    # Login fields

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        """
        This string is used when a `User` is printed in the console.
        """
        return self.email

    @property
    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return self.username

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.username
