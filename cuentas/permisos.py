from django.contrib.auth.models import Group, Permission

NOMBRE_GRUPO_TECNICOS = 'Técnicos'


def obtener_grupo_tecnicos():
    """Devuelve el grupo 'Técnicos' con permiso solo sobre el catálogo de cultivos.
    Si el grupo no existe, lo crea."""
    grupo, _ = Group.objects.get_or_create(name=NOMBRE_GRUPO_TECNICOS)
    grupo.permissions.set(
        Permission.objects.filter(content_type__app_label='cultivos')
    )
    return grupo


def sincronizar_permisos(perfil):
    """Técnico: entra al panel y pertenece al grupo Técnicos.
    Administrador / Superusuario: acceso al panel y fuera del grupo Técnicos.
    Otros roles: sin panel y fuera del grupo."""
    usuario = perfil.usuario
    grupo = obtener_grupo_tecnicos()

    if perfil.rol == perfil.Rol.TECNICO:
        usuario.groups.add(grupo)
        if not usuario.is_staff:
            usuario.is_staff = True
            usuario.save(update_fields=['is_staff'])
    elif perfil.rol == perfil.Rol.ADMINISTRADOR or usuario.is_superuser:
        usuario.groups.remove(grupo)
        if not usuario.is_staff:
            usuario.is_staff = True
            usuario.save(update_fields=['is_staff'])
    else:
        usuario.groups.remove(grupo)
        if usuario.is_staff and not usuario.is_superuser:
            usuario.is_staff = False
            usuario.save(update_fields=['is_staff'])
