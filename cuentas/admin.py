from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Perfil

admin.site.site_header = 'AgroValle — Panel de gestión'
admin.site.site_title = 'AgroValle'
admin.site.index_title = 'Administración'

Usuario = get_user_model()


class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'perfil'


class UsuarioAdmin(UserAdmin):
    inlines = [PerfilInline]
    list_display = ['email', 'first_name', 'last_name', 'rol', 'is_active']
    list_filter = ['perfil__rol', 'is_active', 'is_staff']

    @admin.display(description='Rol')
    def rol(self, obj):
        perfil = getattr(obj, 'perfil', None)
        return perfil.get_rol_display() if perfil else '—'

    def get_inline_instances(self, request, obj=None):
        # Al crear un usuario el perfil se genera solo; el inline aparece al editarlo.
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
