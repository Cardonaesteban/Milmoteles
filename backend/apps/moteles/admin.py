from django.contrib import admin
from .models import Motel, Tarifa


class TarifaInline(admin.TabularInline):
    model = Tarifa
    extra = 1
    fields = ('tipo_habitacion', 'duracion_tipo', 'precio', 'dias_aplicables', 'es_promocion', 'activo', 'ultima_actualizacion')
    readonly_fields = ('ultima_actualizacion',)


@admin.register(Motel)
class MotelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sector', 'telefono', 'calificacion_promedio', 'activo', 'actualizado_en')
    list_filter = ('sector', 'activo')
    search_fields = ('nombre', 'sector', 'direccion')
    prepopulated_fields = {'slug': ('nombre',)}
    inlines = [TarifaInline]


@admin.register(Tarifa)
class TarifaAdmin(admin.ModelAdmin):
    list_display = ('motel', 'tipo_habitacion', 'duracion_tipo', 'precio', 'es_promocion', 'activo', 'ultima_actualizacion')
    list_filter = ('duracion_tipo', 'es_promocion', 'activo')
    search_fields = ('motel__nombre', 'tipo_habitacion')
    readonly_fields = ('ultima_actualizacion', 'creado_en')
