from django.db import models
from django.core.validators import MinValueValidator


class Cultivo(models.Model):
    """Cada cultivo del catálogo: papa, maíz, zanahoria, etc."""

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(
        default=True,
        help_text='Desmarcar para ocultar el cultivo sin borrarlo.',
    )

    class Meta:
        verbose_name = 'cultivo'
        verbose_name_plural = 'cultivos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    @property
    def duracion_total(self):
        """Suma de los días de todas sus etapas."""
        return sum(etapa.dias_duracion for etapa in self.etapas.all())


class Etapa(models.Model):
    """Etapas propias de cada cultivo, en orden.
    Cada cultivo define sus propias etapas, con sus días e información."""

    cultivo = models.ForeignKey(
        Cultivo,
        on_delete=models.CASCADE,
        related_name='etapas',
    )
    orden = models.PositiveIntegerField(
        help_text='Posición de la etapa: 1 = primera, 2 = segunda...',
    )
    nombre = models.CharField(max_length=100)
    dias_duracion = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text='Días fijos que dura la etapa.',
    )
    dias_extension = models.PositiveIntegerField(
        default=3,
        help_text='Días que se agregan si el productor indica que aún no está lista.',
    )
    descripcion = models.TextField(
        blank=True,
        help_text='Qué ocurre con la planta en esta etapa.',
    )
    cuidados = models.TextField(
        blank=True,
        help_text='Qué debe hacer el productor: riego, aporque, deshierbe, etc.',
    )

    class Meta:
        verbose_name = 'etapa'
        verbose_name_plural = 'etapas'
        ordering = ['cultivo', 'orden']
        constraints = [
            models.UniqueConstraint(
                fields=['cultivo', 'orden'],
                name='orden_unico_por_cultivo',
            ),
        ]

    def __str__(self):
        return f'{self.cultivo} - {self.orden}. {self.nombre}'


class Producto(models.Model):
    """Productos que se recomiendan: fertilizantes, fungicidas, etc."""

    class Tipo(models.TextChoices):
        FERTILIZANTE = 'fertilizante', 'Fertilizante'
        ABONO = 'abono', 'Abono orgánico'
        FUNGICIDA = 'fungicida', 'Fungicida'
        INSECTICIDA = 'insecticida', 'Insecticida'
        HERBICIDA = 'herbicida', 'Herbicida'
        OTRO = 'otro', 'Otro'

    class Unidad(models.TextChoices):
        GRAMO = 'g', 'gramos (g)'
        KILO = 'kg', 'kilogramos (kg)'
        MILILITRO = 'ml', 'mililitros (ml)'
        LITRO = 'L', 'litros (L)'

    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    unidad = models.CharField(
        max_length=5,
        choices=Unidad.choices,
        help_text='Unidad en la que se mide la dosis de este producto.',
    )
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Recomendacion(models.Model):
    """Qué producto aplicar en una etapa y en qué dosis.
    Ejemplo: 1 g por cada 2 L de agua."""

    class PorUnidad(models.TextChoices):
        LITRO_AGUA = 'L_agua', 'litros de agua'
        HECTAREA = 'ha', 'hectárea'
        METRO2 = 'm2', 'metro cuadrado'
        PLANTA = 'planta', 'planta'

    etapa = models.ForeignKey(
        Etapa,
        on_delete=models.CASCADE,
        related_name='recomendaciones',
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='recomendaciones',
    )
    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Cantidad del producto (en la unidad del producto).',
    )
    por_cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1,
        help_text='Por cada cuánto. Ej.: 2 (para "por cada 2 L de agua").',
    )
    por_unidad = models.CharField(max_length=10, choices=PorUnidad.choices)
    obligatoria = models.BooleanField(
        default=False,
        help_text='Marcar si debe aplicarse sí o sí en esta etapa.',
    )
    instrucciones = models.TextField(
        blank=True,
        help_text='Cómo y cuándo aplicarlo dentro de la etapa.',
    )

    class Meta:
        verbose_name = 'recomendación'
        verbose_name_plural = 'recomendaciones'
        ordering = ['etapa', '-obligatoria', 'producto']

    def __str__(self):
        return f'{self.producto} en {self.etapa.nombre}'

    @property
    def dosis_texto(self):
        """Devuelve la dosis legible, ej.: '1 g por 2 litros de agua'."""
        cantidad = f'{self.cantidad:g}'
        por = f'{self.por_cantidad:g}'
        return (
            f'{cantidad} {self.producto.unidad} por {por} '
            f'{self.get_por_unidad_display()}'
        )
