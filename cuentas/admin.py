from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.sites.models import Site
from allauth.account.models import EmailAddress

from .models import Perfil

# Personalización del Admin general de AgroValle
admin.site.site_header = '🌱 AgroValle'
admin.site.site_title = 'AgroValle — Panel de gestión'
admin.site.index_title = 'Panel de gestión'
admin.site.site_url = '/inicio/'

Usuario = get_user_model()


class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name = 'perfil de usuario'
    verbose_name_plural = 'datos de perfil y rol'
    fields = ['rol', 'telefono', 'comunidad']


class UsuarioAdmin(UserAdmin):
    inlines = [PerfilInline]
    list_display = ['email', 'first_name', 'last_name', 'rol', 'is_active', 'is_staff']
    list_filter = ['perfil__rol', 'is_active', 'is_staff']
    search_fields = ['email', 'first_name', 'last_name', 'username']

    # Estructura limpia: datos personales y rol primero, permisos individuales colapsados
    fieldsets = (
        ('Identificación y credenciales', {
            'fields': ('username', 'password')
        }),
        ('Información personal', {
            'fields': (('first_name', 'last_name'), 'email')
        }),
        ('Estado de la cuenta y rol', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')
        }),
        ('Permisos individuales avanzados', {
            'classes': ('collapse',),
            'description': 'Solo para configuraciones avanzadas del superusuario.',
            'fields': ('user_permissions',),
        }),
        ('Registro en el sistema', {
            'classes': ('collapse',),
            'fields': ('last_login', 'date_joined'),
        }),
    )

    @admin.display(description='Rol en AgroValle')
    def rol(self, obj):
        perfil = getattr(obj, 'perfil', None)
        if not perfil:
            return '—'
        return perfil.get_rol_display()

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []
        return super().get_inline_instances(request, obj)


admin.site.unregister(Usuario)
admin.site.register(Usuario, UsuarioAdmin)


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'rol', 'telefono', 'comunidad']
    list_filter = ['rol']
    search_fields = ['usuario__email', 'usuario__first_name', 'usuario__last_name', 'comunidad']


# --- Restringir modelos técnicos a superusuarios únicamente ---

class SoloSuperusuarioAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_superuser


# Re-registrar modelos técnicos con restricción
try:
    admin.site.unregister(Site)
    admin.site.register(Site, SoloSuperusuarioAdmin)
except admin.sites.NotRegistered:
    pass

try:
    admin.site.unregister(EmailAddress)
    admin.site.register(EmailAddress, SoloSuperusuarioAdmin)
except admin.sites.NotRegistered:
    pass
