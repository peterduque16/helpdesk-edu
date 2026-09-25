import pytest
from app.models.entities import Ticket

def test_normalizacion_y_duplicados():
    t = Ticket(id="1", requester_id="u1")
    t.add_tag(" Python ")
    t.add_tag("PYTHON")
    assert t.tags == ("python",)

def test_rechazo_espacios_blancos():
    t = Ticket(id="2", requester_id="u2")
    with pytest.raises(ValueError):
        t.add_tag("   ")

def test_independencia_instancias():
    t1 = Ticket(id="3", requester_id="u3")
    t2 = Ticket(id="4", requester_id="u4")
    t1.add_tag("python")
    assert t1.tags == ("python",)
    assert t2.tags == ()

def test_reasignacion_publica_falla():
    t = Ticket(id="5", requester_id="u5")
    with pytest.raises(AttributeError):
        t.tags = ("otro",)
