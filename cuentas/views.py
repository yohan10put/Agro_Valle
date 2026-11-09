import secrets

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.db import models, transaction
from django.shortcuts import get_object_or_404, redirect, render

from allauth.account.forms import ResetPasswordForm
from allauth.account.models import EmailAddress

from cultivos.models import Cultivo, Etapa, Producto
from .forms import NuevoTecnicoForm
from .models import Perfil


def es_administrador(usuario):
    return usuario.is_superuser or getattr(getattr(usuario, 'perfil', None), 'rol', None) == Perfil.Rol.ADMINISTRADOR


def portada(request):
    """Página pública de bienvenida."""
    if request.user.is_authenticated:
        return redirect('inicio')
    return render(request, 'cuentas/portada.html')


@login_required
def inicio(request):
    """Envía a cada usuario a su página según su rol."""
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)

    # Administrador
    if request.user.is_superuser or perfil.rol == Perfil.Rol.ADMINISTRADOR:
        Usuario = get_user_model()
        contexto = {
            'perfil': perfil,
            'kpis': {
                'tecnicos': Perfil.objects.filter(rol=Perfil.Rol.TECNICO).count(),
                'productores': Perfil.objects.filter(rol=Perfil.Rol.PRODUCTOR).count(),
                'compradores': Perfil.objects.filter(rol=Perfil.Rol.COMPRADOR).count(),
                'cultivos': Cultivo.objects.filter(activo=True).count(),
                'publicaciones': 0,
            },
            'ultimos_usuarios': Usuario.objects.select_related('perfil').order_by('-date_joined')[:6],
        }
        return render(request, 'cuentas/inicio_admin.html', contexto)

    # Técnico
    if perfil.es_tecnico:
        etapas_sin_recs = Etapa.objects.annotate(num_recs=models.Count('recomendaciones')).filter(num_recs=0).count()
        contexto = {
            'perfil': perfil,
            'kpis': {
                'cultivos_activos': Cultivo.objects.filter(activo=True).count(),
                'total_etapas': Etapa.objects.count(),
                'total_productos': Producto.objects.count(),
                'etapas_sin_recs': etapas_sin_recs,
            },
            'cultivos': Cultivo.objects.prefetch_related('etapas').all()[:6],
        }
        return render(request, 'cuentas/inicio_tecnico.html', contexto)

    # Comprador
    if perfil.es_comprador:
        return render(request, 'cuentas/inicio_comprador.html', {'perfil': perfil})

    # Productor (por defecto)
    return render(request, 'cuentas/inicio_productor.html', {'perfil': perfil})


@login_required
@user_passes_test(es_administrador)
def nuevo_tecnico(request):
    """El administrador registra a un técnico y gestiona sus invitaciones."""
    form = NuevoTecnicoForm(request.POST or None)

    # Acción de reenviar invitación
    if request.method == 'POST' and 'reenviar_email' in request.POST:
        email = request.POST.get('reenviar_email', '').strip().lower()
        Usuario = get_user_model()
        usuario_tecnico = get_object_or_404(Usuario, email__iexact=email)

        send_mail(
            subject='[AgroValle] Enlace de acceso para técnico',
            message=(
                f'Hola {usuario_tecnico.first_name}:\n\n'
                'Se reenvió tu invitación para acceder como técnico en AgroValle.\n'
                'Utiliza el siguiente enlace para crear o actualizar tu contraseña:\n\n'
                'Equipo AgroValle'
            ),
            from_email=None,
            recipient_list=[email],
        )

        reset = ResetPasswordForm(data={'email': email})
        if reset.is_valid():
            reset.save(request)

        messages.success(request, f'Invitación reenviada con éxito a {email}.')
        return redirect('nuevo_tecnico')

    # Registro de nuevo técnico
    if request.method == 'POST' and form.is_valid():
        datos = form.cleaned_data
        email = datos['email']
        Usuario = get_user_model()

        with transaction.atomic():
            usuario = Usuario.objects.create_user(
                username=email,
                email=email,
                password=secrets.token_urlsafe(32),
                first_name=datos['first_name'],
                last_name=datos['last_name'],
            )
            perfil = Perfil.objects.get(usuario=usuario)
            perfil.rol = Perfil.Rol.TECNICO
            perfil.telefono = datos['telefono']
            perfil.save()

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
