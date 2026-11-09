from django.conf import settings
from django.db import models

from .permisos import sincronizar_permisos


class Perfil(models.Model):
    """Datos extra de cada usuario: su rol en el sistema y su contacto."""

    class Rol(models.TextChoices):
        PRODUCTOR = 'productor', 'Productor'
        COMPRADOR = 'comprador', 'Comprador'
        TECNICO = 'tecnico', 'Técnico'

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil',
    )
    rol = models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.PRODUCTOR,
    )
    telefono = models.CharField('teléfono / WhatsApp', max_length=20, blank=True)
    comunidad = models.CharField(
        max_length=100,
        blank=True,
        help_text='Comunidad o zona donde vive o produce.',
    )

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfiles'

    def __str__(self):
        nombre = self.usuario.get_full_name() or self.usuario.email
        return f'{nombre} ({self.get_rol_display()})'

    @property
    def es_productor(self):
        return self.rol == self.Rol.PRODUCTOR

    @property
    def es_comprador(self):
        return self.rol == self.Rol.COMPRADOR

    @property
    def es_tecnico(self):
        return self.rol == self.Rol.TECNICO

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Cada vez que cambia el rol, se ajustan el acceso al panel y el grupo.
        sincronizar_permisos(self)
