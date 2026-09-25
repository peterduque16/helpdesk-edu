class Notifier:
    def notify(self, ticket_id, technician_id):
        raise NotImplementedError

class WebhookNotifier(Notifier):
    def __init__(self):
        self.sent_payloads = []

    def notify(self, ticket_id, technician_id):
        payload = {"ticket_id": ticket_id, "technician_id": technician_id}
        self.sent_payloads.append(payload)
