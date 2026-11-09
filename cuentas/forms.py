from django import forms
from django.contrib.auth import get_user_model

from allauth.account.models import EmailAddress

from .models import Perfil


class RegistroForm(forms.Form):
    """Campos extra del registro público (allauth agrega correo y contraseña).
    Solo permite elegir productor o comprador: un técnico nunca se registra solo."""

    first_name = forms.CharField(
        label='Nombre',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Juan'})
    )
    last_name = forms.CharField(
        label='Apellido',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Pérez'})
    )
    telefono = forms.CharField(
        label='Teléfono / WhatsApp',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '70000000', 'type': 'tel'})
    )
    comunidad = forms.CharField(
        label='Comunidad o zona de producción',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Guadalupe, Pampa Grande...'})
    )
    rol = forms.ChoiceField(
        label='Me registro como',
        choices=[
            (Perfil.Rol.PRODUCTOR, 'Productor'),
            (Perfil.Rol.COMPRADOR, 'Comprador'),
        ],
        widget=forms.RadioSelect,
    )

    def clean(self):
        datos = super().clean()
        if datos.get('rol') == Perfil.Rol.PRODUCTOR and not datos.get('comunidad'):
            self.add_error('comunidad', 'Por favor indica tu comunidad o zona de producción.')
        return datos

    def signup(self, request, user):
        """allauth llama a este método después de crear el usuario."""
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        perfil, _ = Perfil.objects.get_or_create(usuario=user)
        perfil.rol = self.cleaned_data['rol']
        perfil.telefono = self.cleaned_data['telefono']
        perfil.comunidad = self.cleaned_data['comunidad']
        perfil.save()


class NuevoTecnicoForm(forms.Form):
    """Formulario que usa el administrador para dar de alta a un técnico."""

    first_name = forms.CharField(
        label='Nombre',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Carlos'})
    )
    last_name = forms.CharField(
        label='Apellido',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Mendoza'})
    )
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tecnico@agrovalle.com'})
    )
    telefono = forms.CharField(
        label='Teléfono / WhatsApp',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '70000000', 'type': 'tel'})
    )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        Usuario = get_user_model()
        if (
            Usuario.objects.filter(email__iexact=email).exists()
            or EmailAddress.objects.filter(email__iexact=email).exists()
        ):
            raise forms.ValidationError('Ya existe una cuenta con este correo.')
        return email
