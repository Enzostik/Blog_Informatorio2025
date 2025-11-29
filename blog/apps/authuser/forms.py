import re
from django.core.exceptions import ValidationError

from django import forms
from .models import User
from django.core.validators import validate_email


INVALID_CHR = r'[/\\\*\?"<>|@%"\'\s]'

MSG_ERROR = {
    'user_long'     :   'El usuario debe tener menos de 50 caracteres.',
    'user_chr'      :   'El usuario no puede tener espacios ni los caracteres: /, \\, *, ?, <, >, |, @, ", \'',
    'repeated_user' :   'Este nombre de usuario ya está registrado',
    'invalid_email' :   'Ingrese un correo electrónico válido',
    'repeated_email':   'Este correo electrónico ya está registrado',
    'invalid_pass'  :   'Ingrese una contraseña válida de 8 o más caracteres.',
    'password_chr'  :   'La contraseña debe tener al menos una letra mayúscula, minúscula, números 0-9 y algún caracter especial',
    'not_match'     :   'Las contraseñas no coinciden.',
}
        
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    email = forms.CharField(max_length=150, required=True, widget=forms.EmailInput)
    first_name = forms.CharField(max_length=70, required=True)
    last_name = forms.CharField(max_length=70, required=True)
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput, help_text='Ingrese una contraseña de 8 o más caracteres')
    password_confirm = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput, help_text='Vuelva a ingresar la contraseña.')

    def clean(self):
        #Para validar el formulario lo que se hace es obtener todos los valores cargados
        #Para posteriormente realizar verificaciones de cada valor y devolviendo errores en caso contrario
        #Si hay errores el formulario devuelve falso en is_valid() evitando que se procese
        #Obtener los valores del formulario
        super().clean()
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        #Validar username
        if username:
            #Que el nombre de usuario tenga menos de 50 caracteres
            if len(username)>50:
                self.add_error('username', MSG_ERROR['user_long'])
            #Que no tenga caracteres inválidos
            if re.search(INVALID_CHR, username):
                self.add_error('username', MSG_ERROR['user_chr'])
            #Que no exista en la base de datos
            if User.objects.filter(username=username).exists():
                self.add_error('username', MSG_ERROR['repeated_user'])

        #Validar email
        if email:
            #Que sea un correo electrónico válido
            try:
                validate_email(email)
            except:
                self.add_error('email', MSG_ERROR['invalid_email'])
            #Que no se encuentre registrado en la base de datos
            if User.objects.filter(email=email).exists():
                self.add_error('email', MSG_ERROR['repeated_email'])

        #Los campos first_name y last_name por defecto correrán una verificación al ser required=True
        #Por lo que no es necesario correrla a menos que se quiera verificar algo más

        #Validar los campos contraseña y repetir contraseña
        if password and password_confirm:
            #Verificar que la contraseña cumpla con los requisitos
            if len(password)<8:
                self.add_error('password', MSG_ERROR['invalid_pass'])
            #Comprobar que tenga mayuscula, minuscula, algun caracter especial y al menos un número
            _p = str(password)
            if not (not _p.islower() and not _p.isupper()) or not bool(re.search(r'\d', _p)) or not bool(re.search(r'\W+', _p)):
                self.add_error('password', MSG_ERROR['password_chr'])
            #Verificar que coincidan
            if password != password_confirm:
                self.add_error('password_confirm', MSG_ERROR['not_match'])

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=100, required=True,  widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False, initial=False)