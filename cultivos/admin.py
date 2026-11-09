from django.contrib import admin
from django.utils.html import format_html

from .models import Cultivo, Etapa, Producto, Recomendacion


# --- Etapas dentro de la pantalla del cultivo ---

class EtapaInline(admin.StackedInline):
    model = Etapa
    extra = 1
    fields = [
        ('orden', 'nombre'),
        ('dias_duracion', 'dias_extension'),
        'descripcion',
        'cuidados',
    ]
    show_change_link = True
    verbose_name = 'etapa fenológica'
    verbose_name_plural = 'etapas fenológicas del cultivo (pasos numerados)'


@admin.register(Cultivo)
class CultivoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cantidad_etapas', 'duracion_total_dias', 'estado_activo']
    list_filter = ['activo']
    search_fields = ['nombre']
    inlines = [EtapaInline]

    @admin.display(description='Etapas')
    def cantidad_etapas(self, obj):
        count = obj.etapas.count()
        return format_html('<span style="font-weight: 600;">{} {}</span>', count, 'etapa' if count == 1 else 'etapas')

    @admin.display(description='Duración total (días)')
    def duracion_total_dias(self, obj):
        return f'{obj.duracion_total} días'

    @admin.display(description='Activo', boolean=True)
    def estado_activo(self, obj):
        return obj.activo


# --- Recomendaciones dentro de la pantalla de la etapa ---

class RecomendacionInline(admin.TabularInline):
    model = Recomendacion
    extra = 1
    fields = [
        'producto', 'cantidad', 'por_cantidad', 'por_unidad',
        'obligatoria', 'instrucciones',
    ]
    autocomplete_fields = ['producto']
    verbose_name = 'recomendación técnica'
    verbose_name_plural = 'recomendaciones de aplicación y dosis'


@admin.register(Etapa)
class EtapaAdmin(admin.ModelAdmin):
    list_display = ['cultivo', 'orden', 'nombre', 'dias_duracion', 'dias_extension', 'total_recomendaciones']
    list_filter = ['cultivo']
    search_fields = ['nombre', 'cultivo__nombre']
    fields = [
        'cultivo',
        ('orden', 'nombre'),
        ('dias_duracion', 'dias_extension'),
        'descripcion',
        'cuidados',
    ]
    inlines = [RecomendacionInline]

    @admin.display(description='Recomendaciones')
    def total_recomendaciones(self, obj):
        count = obj.recomendaciones.count()
        if count == 0:
            return format_html('<span style="color: var(--av-danger, #C62828); font-weight: 600;">⚠️ 0 dosis</span>')
        return format_html('<span style="color: var(--av-primary, #2E7D32); font-weight: 600;">{} dosis</span>', count)


# --- Productos e Insumos ---

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'unidad']
    list_filter = ['tipo']
    search_fields = ['nombre']


# --- Recomendaciones directas ---

@admin.register(Recomendacion)
class RecomendacionAdmin(admin.ModelAdmin):
    list_display = ['etapa', 'producto', 'dosis_completa', 'obligatoria']
    list_filter = ['obligatoria', 'etapa__cultivo', 'producto__tipo']
    search_fields = ['etapa__nombre', 'producto__nombre', 'instrucciones']
    autocomplete_fields = ['producto', 'etapa']

    @admin.display(description='Dosis recomendada')
    def dosis_completa(self, obj):
        return obj.dosis_texto
