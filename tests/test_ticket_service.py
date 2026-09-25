import pytest
from app.services.tickets import TicketService
from app.services.notifications import WebhookNotifier
from app.domain.errors import DuplicateAssignmentError
from app.models.entities import User, Ticket

def test_reasignacion_duplicada_falla():
    repo_tickets = {"1": Ticket("1", requester_id="u1", assigned_id="u2")}
    repo_users = {"u1": User("u1", "Alice"), "u2": User("u2", "Bob")}
    notifier = WebhookNotifier()
    service = TicketService(repo_tickets, repo_users, notifier)

    with pytest.raises(DuplicateAssignmentError):
        service.assign("1", "u2")

    # Verificar que no cambió historial ni notificaciones
    assert notifier.sent_payloads == []

def test_asignacion_valida_notifica():
    repo_tickets = {"1": Ticket("1", requester_id="u1")}
    repo_users = {"u1": User("u1", "Alice"), "u2": User("u2", "Bob")}
    notifier = WebhookNotifier()
    service = TicketService(repo_tickets, repo_users, notifier)

    service.assign("1", "u2")

    # Verificar que sí notificó
    assert notifier.sent_payloads == [{"ticket_id": "1", "technician_id": "u2"}]
