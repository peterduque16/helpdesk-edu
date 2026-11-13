
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.database.crear_bd_pruebas import RUTA_BD
from app.database.orm import TicketDB, ArticuloConocimientoDB


engine = create_engine(
    f"sqlite:///{RUTA_BD.as_posix()}"
)

# PASO 1: Guardar un ticket y su artículo
with Session(engine) as session:

    ticket = session.get(TicketDB, "15")

    if ticket is None:
        ticket = TicketDB(
            id="15",
            requester_id="usuario1",
            estado="resuelto"
        )
        session.add(ticket)

    articulo = session.get(ArticuloConocimientoDB, "1")

    if articulo is None:
        articulo = ArticuloConocimientoDB(
            id="1",
            ticket_id="15",
            titulo="Problemas de Wi-Fi",
            solucion="Reiniciar el adaptador"
        )
        session.add(articulo)

    session.commit()

print("Ticket y artículo guardados correctamente")


# PASO 2: Abrir otra sesión y recuperar el artículo
with Session(engine) as session:

    articulo = session.scalar(
        select(ArticuloConocimientoDB).where(
            ArticuloConocimientoDB.titulo.ilike("%Wi-Fi%")
        )
    )

    if articulo is None:
        raise RuntimeError("No se encontró el artículo")

    print("Artículo recuperado:")
    print("ID:", articulo.id)
    print("Ticket:", articulo.ticket_id)
    print("Título:", articulo.titulo)
    print("Solución:", articulo.solucion)
