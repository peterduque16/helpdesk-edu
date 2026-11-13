
from pathlib import Path

from sqlalchemy import create_engine
from app.database.orm import Base

# Ubicación de la base de datos de pruebas
RUTA_BD = (
    Path(__file__).resolve().parents[2]
    / "helpdesk_pruebas.db"
)

# Conexión exclusiva para pruebas
engine = create_engine(
    f"sqlite:///{RUTA_BD.as_posix()}"
)

# Crear las tablas si todavía no existen
Base.metadata.create_all(engine)

print("Base de datos de pruebas creada correctamente")
print("Tablas:", list(Base.metadata.tables.keys()))
