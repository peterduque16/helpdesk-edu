import pytest
from app.models.entities import Ticket
from app.domain.errors import ValidationError

def test_normalizacion_y_duplicados():
    t = Ticket()
    t.add_tag(" Python ")
    t.add_tag("PYTHON")
    assert t.tags == ("python",)

def test_rechazo_espacios_blancos():
    t = Ticket()
    with pytest.raises(ValidationError):
        t.add_tag("   ")

def test_independencia_instancias():
    t1 = Ticket()
    t2 = Ticket()
    t1.add_tag("uno")
    t2.add_tag("dos")
    assert t1.tags == ("uno",)
    assert t2.tags == ("dos",)

def test_reasignacion_publica_falla():
    t = Ticket()
    with pytest.raises(AttributeError):
        t.tags = ["nuevo"]
