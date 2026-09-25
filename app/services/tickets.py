from app.domain.errors import DuplicateAssignmentError

class TicketService:
    def __init__(self, tickets_repo, users_repo, notifier):
        self._tickets = tickets_repo
        self._users = users_repo
        self._notifier = notifier

    def require(self, ticket_id):
        ticket = self._tickets.get(ticket_id)
        if ticket is None:
            raise Exception("Ticket inexistente")
        return ticket

    def watchers(self, ticket_id):
        ticket = self.require(ticket_id)
        usuarios = []

        requester = self._users.require(ticket.requester_id)
        usuarios.append(requester)

        if ticket.assigned_id is not None:
            assigned = self._users.require(ticket.assigned_id)
            if assigned.id != requester.id:
                usuarios.append(assigned)

        return usuarios

    def assign(self, ticket_id, technician_id):
        ticket = self.require(ticket_id)

        # Validación: no asignar al mismo técnico
        if ticket.assigned_id == technician_id:
            raise DuplicateAssignmentError("El ticket ya está asignado a ese técnico")

        # Asignar y notificar
        ticket.assigned_id = technician_id
        self._notifier.notify(ticket_id, technician_id)
