from django.apps import AppConfig


class CuentasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cuentas'
    verbose_name = 'Personas y Accesos'

    def ready(self):
        from . import signals  # noqa: F401  (activa la creación automática del perfil)
