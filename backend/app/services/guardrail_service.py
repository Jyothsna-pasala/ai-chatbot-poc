class GuardrailService:

    def __init__(self):

        # Blocked keywords
        self.blocked_keywords = [
            "disable logging",
            "access host",
            "reset all environments",
            "bypass security",
            "hack",
            "shutdown system"
        ]


    def check(self, message: str):

        message_lower = message.lower()

        for keyword in self.blocked_keywords:

            if keyword in message_lower:

                return {
                    "blocked": True,
                    "reason": f"Blocked due to restricted operation: {keyword}"
                }

        return {
            "blocked": False,
            "reason": None
        }