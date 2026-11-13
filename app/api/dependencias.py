
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

RUTA_BD = Path(__file__).resolve().parents[2] / "helpdesk_pruebas.db"

engine = create_engine(
    f"sqlite:///{RUTA_BD.as_posix()}",
    connect_args={"check_same_thread": False}
)


def obtener_sesion():
    with Session(engine) as session:
        yield session
