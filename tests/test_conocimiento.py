
import pytest

from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session

from app.database.orm import (
    Base,
    TicketDB,
    ArticuloConocimientoDB,
)
from app.repositories.articulos import ArticuloRepository
from app.repositories.tickets import TicketRepository
from app.services.conocimiento import ConocimientoService


def test_publicar_y_rechazar_ticket_abierto(tmp_path):
    # Crear una base de datos temporal
    ruta = tmp_path / "prueba_conocimiento.db"
    engine = create_engine(f"sqlite:///{ruta.as_posix()}")

    Base.metadata.create_all(engine)

    # Preparar dos tickets de prueba
    with Session(engine) as session:
        session.add_all([
            TicketDB(
                id="100",
                requester_id="usuario1",
                estado="resuelto"
            ),
            TicketDB(
                id="200",
                requester_id="usuario2",
                estado="abierto"
            ),
        ])
        session.commit()

    # Probar la publicación
    with Session(engine) as session:
        articulos = ArticuloRepository(session)
        tickets = TicketRepository(session)

        servicio = ConocimientoService(articulos, tickets)

        # CASO 1: ticket resuelto
        articulo = servicio.publicar(
            ticket_id="100",
            titulo="Problema de Internet",
            solucion="Reiniciar el router",
            rol="tecnico"
        )

        session.commit()

        assert articulo.titulo == "Problema de Internet"

        # Contar artículos guardados
        cantidad_antes = session.scalar(
            select(func.count()).select_from(
                ArticuloConocimientoDB
            )
        )

        # CASO 2: ticket abierto
        with pytest.raises(ValueError):
            servicio.publicar(
                ticket_id="200",
                titulo="Artículo no permitido",
                solucion="Esta solución no debe guardarse",
                rol="tecnico"
            )

        cantidad_despues = session.scalar(
            select(func.count()).select_from(
                ArticuloConocimientoDB
            )
        )

        assert cantidad_antes == cantidad_despues

    # CASO 3: recuperar desde otra sesión
    with Session(engine) as session:
        repo = ArticuloRepository(session)
        encontrados = repo.buscar_por_titulo("Internet")

        assert len(encontrados) == 1
        assert encontrados[0].ticket_id == "100"

    engine.dispose()


def test_usuario_sin_permiso_no_publica(tmp_path):
    ruta = tmp_path / "permisos.db"
    engine = create_engine(f"sqlite:///{ruta.as_posix()}")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(
            TicketDB(
                id="300",
                requester_id="usuario3",
                estado="resuelto"
            )
        )
        session.commit()

    with Session(engine) as session:
        articulos = ArticuloRepository(session)
        tickets = TicketRepository(session)
        servicio = ConocimientoService(articulos, tickets)

        # Un usuario normal intenta publicar
        with pytest.raises(PermissionError):
            servicio.publicar(
                ticket_id="300",
                titulo="Artículo prohibido",
                solucion="No debe guardarse",
                rol="usuario"
            )

        # Comprobar que no se guardó nada
        cantidad = session.scalar(
            select(func.count()).select_from(
                ArticuloConocimientoDB
            )
        )

        assert cantidad == 0

    engine.dispose()

