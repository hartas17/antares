import jwt
from django.contrib import messages
from jwt import InvalidSignatureError
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render
from django.template import loader
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken

from .models import User
from .serializers import CustomJWTSerializer, UserSerializer, UserCreateSerializer, UserChangePasswordSerializer
from .forms import ResetPasswordForm


class UserCreate(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            user.username = user.email
            user.save()

            if settings.CUSTOM_REGISTRATION.get('SEND_ACTIVATION_EMAIL', False):
                send_activation_email(
                    user_email=user.email,
                    activation_code=user.activation_token,
                    site=get_current_site(request)
                )
            else:
                user.is_active = True
                user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserResetPassword(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        if not email:
            error = {'email': ['This field is required.']}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.filter(email=email).first()
            if user:
                site = get_current_site(request)
                send_reset_password_email(user, site=site)
                return Response({'email': email}, status=status.HTTP_200_OK)
            else:
                return Response({'email': email}, status=status.HTTP_200_OK)


class UserChangePassword(APIView):
    queryset = User.objects.none()
    permission_classes = []

    def post(self, request):
        serializer = UserChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.data['new_password'])
            user.save()
            return Response({'message': 'Password changed.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Me(APIView):
    permission_classes = []

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


def send_activation_email(user_email, activation_code, site):
    activation_url = f'{site.domain}/activate/{activation_code}/'
    html_message = loader.render_to_string('registration/activation_email.html', {'activation_url': activation_url})
    recipient_list = [user_email]
    send_mail(
        subject='Código de activación',
        message='Código de activación',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False,
        html_message=html_message
    )


def activation(request, activation_token):
    try:
        user = User.objects.get(activation_token=activation_token)
        if not user.is_active:
            user.is_active = True
            user.save()
        current_site = get_current_site(request)
        context = {
            'site_name': current_site.name,
            'site_domain': current_site.domain
        }
        return render(request, 'registration/activation.html', context=context)
    except User.DoesNotExist:
        raise Http404('User not found.')


def send_reset_password_email(user, site):
    token = jwt.encode({'user_id': user.pk}, user.password, algorithm='HS256').decode('utf-8')
    reset_url = f'{site.domain}/reset-password/{user.pk}/{token}/'
    html_message = loader.render_to_string('registration/reset_password_email.html', {'reset_url': reset_url})

    recipient_list = [user.email]
    send_mail(
        subject='Restablece tu contraseña',
        message='Restablece tu contraseña',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False,
        html_message=html_message
    )


def reset_password(request, user_id, token):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)

        try:
            jwt.decode(token, user.password, algorithms='HS256')
        except InvalidSignatureError:
            form = ResetPasswordForm()
            messages.error(request, 'El link para cambiar contraseña ya no es válido.')
            return render(request, 'registration/reset_password.html', {'form': form})

        if form.is_valid():
            new_password = form.cleaned_data.get('password')
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Contraseña actualizada de forma correcta.')
            return render(request, 'registration/reset_password.html', {'form': form})
    else:
        form = ResetPasswordForm(initial={'token': token})

    return render(request, 'registration/reset_password.html', {'form': form})


obtain_jwt_token = ObtainJSONWebToken.as_view(serializer_class=CustomJWTSerializer)
