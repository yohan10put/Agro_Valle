from django.contrib import admin

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
    show_change_link = True  # enlace para abrir la etapa y cargar sus recomendaciones


@admin.register(Cultivo)
class CultivoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cantidad_etapas', 'duracion_total_dias', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']
    inlines = [EtapaInline]

    @admin.display(description='Etapas')
    def cantidad_etapas(self, obj):
        return obj.etapas.count()

    @admin.display(description='Duración total (días)')
    def duracion_total_dias(self, obj):
        return obj.duracion_total


# --- Recomendaciones dentro de la pantalla de la etapa ---

class RecomendacionInline(admin.TabularInline):
    model = Recomendacion
    extra = 1
    fields = [
        'producto', 'cantidad', 'por_cantidad', 'por_unidad',
        'obligatoria', 'instrucciones',
    ]
    autocomplete_fields = ['producto']


@admin.register(Etapa)
class EtapaAdmin(admin.ModelAdmin):
    list_display = ['cultivo', 'orden', 'nombre', 'dias_duracion', 'dias_extension']
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


# --- Productos ---

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'unidad']
    list_filter = ['tipo']
    search_fields = ['nombre']  # necesario para el buscador en recomendaciones
