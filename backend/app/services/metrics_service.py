class MetricsService:

    def __init__(self):
        self.total_conversations = 0
        self.escalations = 0
        self.guardrail_blocks = 0
        self.tickets_created = 0

        self.severity_counts = {
            "LOW": 0,
            "MEDIUM": 0,
            "HIGH": 0
        }

    def record_chat(self):
        self.total_conversations += 1

    def record_guardrail(self):
        self.guardrail_blocks += 1

    def record_escalation(self):
        self.escalations += 1

    def record_ticket(self, severity):
        self.tickets_created += 1
        if severity in self.severity_counts:
            self.severity_counts[severity] += 1

    def get_summary(self):
        return {
            "totalConversations": self.total_conversations,
            "escalations": self.escalations,
            "guardrailBlocks": self.guardrail_blocks,
            "ticketsCreated": self.tickets_created,
            "severityCounts": self.severity_counts
        }

    def get_trends(self):
        return {
            "conversations": self.total_conversations,
            "tickets": self.tickets_created,
            "guardrailTriggers": self.guardrail_blocks
        }