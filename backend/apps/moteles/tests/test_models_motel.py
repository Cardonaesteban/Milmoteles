import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from apps.moteles.models import Motel


@pytest.mark.django_db
class TestMotelModel:
    """Suite de pruebas unitarias para el modelo Motel."""

    def test_motel_creation_success(self):
        """Verifica la creación exitosa de un motel con todos sus campos completos."""
        motel = Motel.objects.create(
            nombre="Motel Los Almendros",
            descripcion="Suites de lujo con jacuzzi y servicio a la habitación.",
            direccion="Calle 10 # 43E-20",
            sector="Poblado",
            telefono="+57 300 123 4567",
            whatsapp="+57 300 123 4567",
            email="contacto@losalmendros.com",
            latitud=Decimal("6.208500"),
            longitud=Decimal("-75.567800"),
            calificacion_promedio=Decimal("4.80"),
            activo=True,
        )

        assert motel.id is not None
        assert motel.nombre == "Motel Los Almendros"
        assert motel.slug == "motel-los-almendros"
        assert motel.sector == "Poblado"
        assert motel.activo is True
        assert motel.creado_en is not None
        assert motel.actualizado_en is not None

    def test_motel_slug_auto_generation(self):
        """Verifica que el slug se autogenere a partir del nombre en formato kebab-case."""
        motel = Motel.objects.create(
            nombre="Motel Jardín del Edén",
            direccion="Carrera 70 # 32-15",
            sector="Laureles",
            telefono="6044445566",
        )
        assert motel.slug == "motel-jardin-del-eden"

    def test_motel_slug_unique_on_conflict(self):
        """Verifica que moteles con nombres idénticos generen slugs únicos correlativos."""
        motel1 = Motel.objects.create(
            nombre="Motel Paraíso",
            direccion="Calle 30 # 65-10",
            sector="Belén",
            telefono="6042223344",
        )
        motel2 = Motel.objects.create(
            nombre="Motel Paraíso",
            direccion="Carrera 45 # 50-20",
            sector="Centro",
            telefono="6043334455",
        )

        assert motel1.slug == "motel-paraiso"
        assert motel2.slug == "motel-paraiso-1"

    def test_motel_str_representation(self):
        """Verifica que __str__ devuelva el formato 'Nombre (Sector)'."""
        motel = Motel(
            nombre="Motel La Cabaña",
            sector="Guayabal",
            direccion="Calle 12 Sur # 50-30",
            telefono="6041112233",
        )
        assert str(motel) == "Motel La Cabaña (Guayabal)"

    def test_motel_default_calificacion_and_activo(self):
        """Verifica los valores predeterminados de calificación (0.00) y estado activo (True)."""
        motel = Motel.objects.create(
            nombre="Motel Oasis",
            direccion="Autopista Sur # 80-12",
            sector="Itagüí",
            telefono="6049998877",
        )
        assert motel.calificacion_promedio == Decimal("0.00")
        assert motel.activo is True

    def test_motel_calificacion_max_valida(self):
        """Verifica que calificaciones superiores a 5.00 fallen la validación."""
        motel = Motel(
            nombre="Motel Glamour",
            direccion="Circular 4 # 72-10",
            sector="Laureles",
            telefono="6047778899",
            calificacion_promedio=Decimal("5.50"),
        )
        with pytest.raises(ValidationError):
            motel.full_clean()

    def test_motel_calificacion_negativa_invalida(self):
        """Verifica que calificaciones menores a 0.00 fallen la validación."""
        motel = Motel(
            nombre="Motel Glamour Negativo",
            direccion="Circular 4 # 72-10",
            sector="Laureles",
            telefono="6047778899",
            calificacion_promedio=Decimal("-1.00"),
        )
        with pytest.raises(ValidationError):
            motel.full_clean()

    def test_motel_nombre_min_length(self):
        """Verifica que un nombre menor a 2 caracteres falle la validación."""
        motel = Motel(
            nombre="M",
            direccion="Calle 1 # 2-3",
            sector="Centro",
            telefono="6040001122",
        )
        with pytest.raises(ValidationError):
            motel.full_clean()
