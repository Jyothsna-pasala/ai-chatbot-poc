import uuid
from datetime import datetime


class TicketService:

    def __init__(self):
        self.tickets = []

    def create_ticket(self, session_id, issue, severity, tier):

        ticket_id = f"TICKET-{uuid.uuid4().hex[:8].upper()}"

        ticket = {
            "ticketId": ticket_id,
            "sessionId": session_id,
            "issue": issue,
            "severity": severity,
            "tier": tier,
            "createdAt": datetime.utcnow().isoformat()
        }

        self.tickets.append(ticket)

        return ticket

    def get_all_tickets(self):
        return self.tickets