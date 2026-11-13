
from uuid import uuid4

from app.database.orm import ArticuloConocimientoDB


class ConocimientoService:

    ROLES_PERMITIDOS = {
        "tecnico",
        "supervisor",
        "administrador"
    }

    def __init__(self, articulos_repo, tickets_repo):
        self.articulos = articulos_repo
        self.tickets = tickets_repo

    def publicar(self, ticket_id, titulo, solucion, rol):
        # Primero: comprobar quién quiere publicar
        if rol not in self.ROLES_PERMITIDOS:
            raise PermissionError(
                "No tienes permiso para publicar artículos"
            )

        # Segundo: comprobar que existe el ticket
        ticket = self.tickets.obtener_por_id(ticket_id)

        if ticket is None:
            raise ValueError("El ticket no existe")

        # Tercero: comprobar que está resuelto
        if ticket.estado != "resuelto":
            raise ValueError(
                "Solo se pueden publicar artículos de tickets resueltos"
            )

        # Cuarto: comprobar los campos
        if not titulo or not titulo.strip():
            raise ValueError("El título es obligatorio")

        if not solucion or not solucion.strip():
            raise ValueError("La solución es obligatoria")

        # Quinto: preparar el artículo
        articulo = ArticuloConocimientoDB(
            id=str(uuid4()),
            ticket_id=ticket_id,
            titulo=titulo.strip(),
            solucion=solucion.strip()
        )

        return self.articulos.crear(articulo)
