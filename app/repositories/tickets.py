
from app.database.orm import TicketDB


class TicketRepository:

    def __init__(self, session):
        self.session = session

    def obtener_por_id(self, ticket_id):
        return self.session.get(TicketDB, ticket_id)
