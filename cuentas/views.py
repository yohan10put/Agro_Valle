import secrets

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import redirect, render

from allauth.account.forms import ResetPasswordForm
from allauth.account.models import EmailAddress

from .forms import NuevoTecnicoForm
from .models import Perfil


def es_administrador(usuario):
    return usuario.is_superuser


def portada(request):
    """Página pública de bienvenida."""
    if request.user.is_authenticated:
        return redirect('inicio')
    return render(request, 'cuentas/portada.html')


@login_required
def inicio(request):
    """Envía a cada usuario a su página según su rol."""
    if request.user.is_superuser:
        return render(request, 'cuentas/inicio_admin.html')

    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)

    if perfil.es_tecnico:
        return redirect('admin:index')
    if perfil.es_comprador:
        return render(request, 'cuentas/inicio_comprador.html', {'perfil': perfil})
    return render(request, 'cuentas/inicio_productor.html', {'perfil': perfil})


@login_required
@user_passes_test(es_administrador)
def nuevo_tecnico(request):
    """El administrador registra a un técnico.
    El técnico recibe un correo para crear su propia contraseña."""
    form = NuevoTecnicoForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        datos = form.cleaned_data
        email = datos['email']
        Usuario = get_user_model()

        with transaction.atomic():
            usuario = Usuario.objects.create_user(
                username=email,
                email=email,
                # Contraseña aleatoria que nadie conoce: el técnico crea la suya por correo.
                password=secrets.token_urlsafe(32),
                first_name=datos['first_name'],
                last_name=datos['last_name'],
            )
            perfil = Perfil.objects.get(usuario=usuario)
            perfil.rol = Perfil.Rol.TECNICO
            perfil.telefono = datos['telefono']
            perfil.save()

            # El correo se marca como verificado: solo quien lo abra podrá crear la contraseña.
            EmailAddress.objects.create(
                user=usuario, email=email, primary=True, verified=True
            )

        send_mail(
            subject='[AgroValle] Bienvenido como técnico',
            message=(
                f'Hola {usuario.first_name}:\n\n'
                'Fuiste registrado como técnico en AgroValle. '
                'En otro correo recibirás un enlace para crear tu contraseña. '
                'Después podrás iniciar sesión con este correo y cargar el '
                'catálogo de cultivos, etapas y recomendaciones.\n\n'
                'Equipo AgroValle'
            ),
            from_email=None,
            recipient_list=[email],
        )

        reset = ResetPasswordForm(data={'email': email})
        if reset.is_valid():
            reset.save(request)

        messages.success(
            request,
            f'Técnico {usuario.get_full_name()} registrado. '
            f'Se enviaron las instrucciones a {email}.',
        )
        return redirect('nuevo_tecnico')

    tecnicos = Perfil.objects.filter(rol=Perfil.Rol.TECNICO).select_related('usuario')
    return render(
        request,
        'cuentas/nuevo_tecnico.html',
        {'form': form, 'tecnicos': tecnicos},
    )
