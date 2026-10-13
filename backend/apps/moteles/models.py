from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify


class Motel(models.Model):
    """
    Representa un establecimiento (Motel) en la plataforma Milmoteles.
    Cumple con requerimientos de SEO (slug), NAP (nombre, dirección, teléfono),
    geolocalización y canales de contacto.
    """
    nombre = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(2)],
        help_text="Nombre comercial del motel"
    )
    slug = models.SlugField(
        max_length=160,
        unique=True,
        blank=True,
        db_index=True,
        help_text="Identificador único para SEO y URLs semánticas [SEO/Title Tag]"
    )
    descripcion = models.TextField(
        blank=True,
        help_text="Descripción detallada de las instalaciones y servicios"
    )
    direccion = models.CharField(
        max_length=255,
        help_text="Dirección física completa [NAP]"
    )
    sector = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Sector o barrio en Medellín (ej. Laureles, Poblado, Guayabal, Centro)"
    )
    telefono = models.CharField(
        max_length=25,
        help_text="Número telefónico principal [NAP, Tel Link]"
    )
    whatsapp = models.CharField(
        max_length=25,
        blank=True,
        help_text="Número de WhatsApp para contacto directo [Live Chat]"
    )
    email = models.EmailField(
        blank=True,
        help_text="Correo electrónico de contacto [Mailto Link]"
    )
    latitud = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Coordenada de latitud para geolocalización"
    )
    longitud = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Coordenada de longitud para geolocalización"
    )
    calificacion_promedio = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('5.00'))],
        help_text="Calificación promedio (0.00 a 5.00) [Social Proof]"
    )
    activo = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Indica si el motel está activo y visible para búsquedas"
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Motel"
        verbose_name_plural = "Moteles"
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['sector', 'activo']),
            models.Index(fields=['slug']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nombre)
            slug = base_slug
            counter = 1
            while Motel.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.sector})"


class Tarifa(models.Model):
    """
    Representa una tarifa asociada a un motel y una duración específica.
    Regla crítica de negocio:
    - Precios estrictamente mayores a cero (> 0).
    - Duraciones explícitas y normalizadas (no equivalentes).
    - Registro de última actualización obligatorio para fiabilidad de comparación.
    """
    class DuracionTipo(models.TextChoices):
        DOS_HORAS = '2_HORAS', '2 Horas'
        TRES_HORAS = '3_HORAS', '3 Horas'
        CUATRO_HORAS = '4_HORAS', '4 Horas'
        SEIS_HORAS = '6_HORAS', '6 Horas'
        DOCE_HORAS = '12_HORAS', '12 Horas'
        AMANECIDA = 'AMANECIDA', 'Amanecida / Noche Completa'
        HORA_ADICIONAL = 'HORA_ADICIONAL', 'Hora Adicional'
        OTRO = 'OTRO', 'Otro período específico'

    motel = models.ForeignKey(
        Motel,
        on_delete=models.CASCADE,
        related_name='tarifas',
        help_text="Motel al que pertenece esta tarifa"
    )
    tipo_habitacion = models.CharField(
        max_length=100,
        default='Estándar',
        help_text="Categoría o tipo de habitación (ej. Estándar, Jacuzzi, Suite, Temática)"
    )
    duracion_tipo = models.CharField(
        max_length=20,
        choices=DuracionTipo.choices,
        default=DuracionTipo.TRES_HORAS,
        db_index=True,
        help_text="Unidad normalizada de duración para comparaciones estrictas"
    )
    duracion_detalle = models.CharField(
        max_length=100,
        blank=True,
        help_text="Detalle legible de la duración (ej. '3 Horas de Domingo a Jueves')"
    )
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Precio en COP de la tarifa (debe ser estrictamente mayor a 0)"
    )
    dias_aplicables = models.CharField(
        max_length=100,
        default='Todos los días',
        help_text="Días u horario en que aplica la tarifa (ej. Lunes a Jueves, Fin de semana)"
    )
    es_promocion = models.BooleanField(
        default=False,
        help_text="Indica si la tarifa corresponde a una promoción u oferta especial"
    )
    ultima_actualizacion = models.DateTimeField(
        auto_now=True,
        db_index=True,
        help_text="Fecha exacta de última actualización de tarifas (regla estricta de validación)"
    )
    activo = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Indica si la tarifa está activa y vigente para reservas"
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tarifa"
        verbose_name_plural = "Tarifas"
        ordering = ['motel', 'precio']
        indexes = [
            models.Index(fields=['motel', 'duracion_tipo', 'activo']),
            models.Index(fields=['precio']),
        ]

    def clean(self):
        super().clean()
        if self.precio is not None and self.precio <= Decimal('0.00'):
            raise ValidationError({'precio': 'El precio de la tarifa debe ser estrictamente mayor a cero.'})
        if not self.duracion_tipo:
            raise ValidationError({'duracion_tipo': 'La tarifa debe especificar una duración normalizada válida.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.motel.nombre} - {self.tipo_habitacion} ({self.get_duracion_tipo_display()}): ${self.precio:,.2f}"
