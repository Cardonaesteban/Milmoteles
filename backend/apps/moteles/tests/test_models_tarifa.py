import pytest
from decimal import Decimal
import time
from django.core.exceptions import ValidationError
from apps.moteles.models import Motel, Tarifa


@pytest.mark.django_db
class TestTarifaModel:
    """Suite de pruebas unitarias para el modelo Tarifa."""

    @pytest.fixture
    def motel(self):
        return Motel.objects.create(
            nombre="Motel Primavera",
            direccion="Calle 50 # 40-10",
            sector="Laureles",
            telefono="6042345678",
        )

    def test_tarifa_creation_success(self, motel):
        """Verifica la creación exitosa de una tarifa asociada a un motel."""
        tarifa = Tarifa.objects.create(
            motel=motel,
            tipo_habitacion="Suite Jacuzzi",
            duracion_tipo=Tarifa.DuracionTipo.TRES_HORAS,
            duracion_detalle="3 Horas en semana",
            precio=Decimal("65000.00"),
            dias_aplicables="Lunes a Jueves",
            es_promocion=False,
            activo=True,
        )

        assert tarifa.id is not None
        assert tarifa.motel == motel
        assert tarifa.tipo_habitacion == "Suite Jacuzzi"
        assert tarifa.duracion_tipo == "3_HORAS"
        assert tarifa.precio == Decimal("65000.00")
        assert tarifa.activo is True
        assert tarifa.ultima_actualizacion is not None

    def test_tarifa_precio_cero_falla(self, motel):
        """Regla de Negocio: El precio de la tarifa no puede ser 0."""
        tarifa = Tarifa(
            motel=motel,
            tipo_habitacion="Sencilla",
            duracion_tipo=Tarifa.DuracionTipo.TRES_HORAS,
            precio=Decimal("0.00"),
        )
        with pytest.raises(ValidationError) as exc_info:
            tarifa.full_clean()
        assert "precio" in exc_info.value.message_dict

    def test_tarifa_precio_negativo_falla(self, motel):
        """Regla de Negocio: El precio no puede ser negativo."""
        tarifa = Tarifa(
            motel=motel,
            tipo_habitacion="Sencilla",
            duracion_tipo=Tarifa.DuracionTipo.TRES_HORAS,
            precio=Decimal("-25000.00"),
        )
        with pytest.raises(ValidationError) as exc_info:
            tarifa.full_clean()
        assert "precio" in exc_info.value.message_dict

    def test_tarifa_duracion_requerida(self, motel):
        """Regla de Negocio: Cada tarifa debe estar asociada a una duración específica."""
        tarifa = Tarifa(
            motel=motel,
            tipo_habitacion="Sencilla",
            duracion_tipo="",
            precio=Decimal("50000.00"),
        )
        with pytest.raises(ValidationError) as exc_info:
            tarifa.full_clean()
        assert "duracion_tipo" in exc_info.value.message_dict

    def test_tarifa_duraciones_distintas_no_equivalentes(self, motel):
        """
        Regla de Negocio: No comparar tarifas con duraciones diferentes como si fueran equivalentes.
        Verifica que coexistan tarifas diferenciadas por duración para el mismo establecimiento.
        """
        tarifa_3h = Tarifa.objects.create(
            motel=motel,
            tipo_habitacion="Estándar",
            duracion_tipo=Tarifa.DuracionTipo.TRES_HORAS,
            precio=Decimal("45000.00"),
        )
        tarifa_amanecida = Tarifa.objects.create(
            motel=motel,
            tipo_habitacion="Estándar",
            duracion_tipo=Tarifa.DuracionTipo.AMANECIDA,
            precio=Decimal("95000.00"),
        )

        assert tarifa_3h.duracion_tipo != tarifa_amanecida.duracion_tipo
        assert tarifa_3h.precio != tarifa_amanecida.precio
        assert motel.tarifas.count() == 2

    def test_tarifa_str_representation(self, motel):
        """Verifica la representación legible en string de la tarifa."""
        tarifa = Tarifa.objects.create(
            motel=motel,
            tipo_habitacion="Suite Presidencial",
            duracion_tipo=Tarifa.DuracionTipo.AMANECIDA,
            precio=Decimal("120000.00"),
        )
        assert "Motel Primavera" in str(tarifa)
        assert "Suite Presidencial" in str(tarifa)
        assert "Amanecida / Noche Completa" in str(tarifa)
        assert "$120,000.00" in str(tarifa)

    def test_tarifa_actualizacion_automatica_timestamp(self, motel):
        """Regla de Negocio: El sistema debe registrar la fecha exacta de última actualización."""
        tarifa = Tarifa.objects.create(
            motel=motel,
            tipo_habitacion="Estándar",
            duracion_tipo=Tarifa.DuracionTipo.TRES_HORAS,
            precio=Decimal("40000.00"),
        )
        primera_fecha = tarifa.ultima_actualizacion

        # Modificación de precio
        time.sleep(0.05)
        tarifa.precio = Decimal("45000.00")
        tarifa.save()
        tarifa.refresh_from_db()

        assert tarifa.ultima_actualizacion > primera_fecha

    def test_tarifa_cascade_deletion(self, motel):
        """Verifica que al eliminar un motel se eliminen en cascada sus tarifas."""
        Tarifa.objects.create(
            motel=motel,
            tipo_habitacion="Estándar",
            duracion_tipo=Tarifa.DuracionTipo.DOS_HORAS,
            precio=Decimal("35000.00"),
        )
        assert Tarifa.objects.filter(motel=motel).count() == 1

        motel.delete()
        assert Tarifa.objects.count() == 0
