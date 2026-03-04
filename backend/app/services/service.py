from app.services.ticket_service import TicketService
from app.services.vector_service import VectorService
from app.services.guardrail_service import GuardrailService
from app.services.metrics_service import MetricsService

# Create single shared instances
ticket_service = TicketService()
vector_service = VectorService()
guardrail_service = GuardrailService()
metrics_service = MetricsService()