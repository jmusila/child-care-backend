import re
from django.contrib.auth import authenticate
from .models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    """ User registration serializers """

    def validate(self, data):
        """ password validator """
        if not any(char.isdigit() for char in data['password']):
            raise serializers.ValidationError(
                "password must contain at least one number.")
        elif re.match(r'^\w+$', data['password']):
            raise serializers.ValidationError(
                "password must contain at least one special character.")
        return data

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """ Handles serialization and deserialization of user object """
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def update(self, instance, validated_data):
        """ User data update """
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()` is the method mentioned above. It handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(password)

            # Finally, after everything has been updated, we must explicitly save
            # the model. It's worth pointing out that `.set_password()` does not
            # save the model.
        instance.save()

        return instance
