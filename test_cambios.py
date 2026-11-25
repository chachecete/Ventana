from datetime import datetime
import pytest

from cambios import dentro_ventana


@pytest.mark.parametrize(
    "fecha,ventana,esperado",
    [
        (
            datetime(2026, 11, 7, 2, 0),
            "#01-07#S,D#S1,S2",
            True,
        ),
        (
            datetime(2026, 11, 14, 6, 0),
            "#01-07#S,D#S1,S2",
            True,
        ),
        (
            datetime(2026, 11, 21, 2, 0),
            "#01-07#S,D#S1,S2",
            False,
        ),
        (
            datetime(2026, 11, 9, 2, 0),
            "#01-07#S,D#S1,S2",
            False,
        ),
    ],
)
def test_ventanas(fecha, ventana, esperado):
    assert dentro_ventana(fecha, ventana) == esperado


@pytest.mark.parametrize(
    "fecha,esperado",
    [
        (datetime(2026, 11, 7, 0, 59), False),
        (datetime(2026, 11, 7, 1, 0), True),
        (datetime(2026, 11, 7, 6, 59), True),
        (datetime(2026, 11, 7, 7, 0), False),
    ],
)
def test_limites_horarios(fecha, esperado):
    assert dentro_ventana(fecha, "#01-07#S,D#S1,S2") == esperado


@pytest.mark.parametrize(
    "fecha,esperado",
    [
        (datetime(2026, 11, 7, 6, 59), False),
        (datetime(2026, 11, 7, 7, 0), True),
        (datetime(2026, 11, 7, 23, 59), True),
        (datetime(2026, 11, 8, 0, 0), True),
        (datetime(2026, 11, 8, 2, 59), True),
        (datetime(2026, 11, 8, 3, 0), False),
    ],
)
def test_ventana_cruza_medianoche(fecha, esperado):
    assert dentro_ventana(fecha, "#07-03#S#S1,S2") == esperado


def test_semana_uno_contiene_el_dia_uno():
    fecha = datetime(2026, 12, 5, 2, 0)  # sábado
    assert dentro_ventana(fecha, "#01-07#S#S1")