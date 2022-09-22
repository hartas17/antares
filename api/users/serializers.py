from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'activation_token')


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name', 'is_staff', 'is_active')

    def create(self, validated_data):
        user = super(UserCreateSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_email(self, value):
        user = User.objects.filter(email=value).exists()
        if user:
            raise serializers.ValidationError(_('The email: %(value)s is already registered.') % {'value': value})
        return value

    def validate_password(self, value):
        request = self.context.get('request', None)
        confirm_password = request.data.get('confirm_password', None)

        if confirm_password != value:
            raise serializers.ValidationError(_('Passwords do not match.'))
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e)

        return value


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate_new_password(self, value):
        request = self.context.get('request', None)
        confirm_new_password = request.data.get('confirm_new_password', None)

        if confirm_new_password != value:
            raise serializers.ValidationError(_('Passwords do not match.'))

        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e)

        return value

    def validate_old_password(self, value):
        request = self.context.get('request', None)
        user = request.user

        if not user.check_password(value):
            raise serializers.ValidationError(_('Old password not match.'))


class CustomJWTSerializer(JSONWebTokenSerializer):
    username_field = 'email'

    def validate(self, attrs):
        password = attrs.get("password")
        user_obj = User.objects.filter(
            email=attrs.get("email")).first() or User.objects.filter(username=attrs.get("email")).first()
        if user_obj is not None:
            credentials = {
                'username': user_obj.username,
                'password': password
            }
            if all(credentials.values()):
                user = authenticate(**credentials)
                if user:
                    if not user.is_active:
                        msg = _('User account is disabled.')
                        raise serializers.ValidationError(msg)

                    payload = jwt_payload_handler(user)

                    return {
                        'token': jwt_encode_handler(payload),
                        'user': user
                    }
                else:
                    msg = _('Unable to log in with provided credentials.')
                    raise serializers.ValidationError(msg)

            else:
                msg = _(f'Must include username and password.')
                raise serializers.ValidationError(msg)

        else:
            msg = _('Account with this email/username does not exists')
            raise serializers.ValidationError(msg)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
