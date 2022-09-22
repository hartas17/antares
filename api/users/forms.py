from django import forms
from django.contrib.auth import password_validation


class ResetPasswordForm(forms.Form):
    password = forms.CharField(label='Contraseña', max_length=100, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirmar contraseña', max_length=100, widget=forms.PasswordInput())
    token = forms.CharField(max_length=1000, widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError('Las contraseñas no coinciden.')

        if password:
            try:
                password_validation.validate_password(password)
            except forms.ValidationError as error:
                self.add_error('password', error)
