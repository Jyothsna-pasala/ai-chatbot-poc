class ClassificationService:

    def classify(self, message: str):

        message_lower = message.lower()

        # Critical infrastructure issues
        if "kernel panic" in message_lower:
            return {"tier": "TIER_3", "severity": "CRITICAL"}

        if "vm crashed" in message_lower or "vm froze" in message_lower:
            return {"tier": "TIER_2", "severity": "HIGH"}

        if "container init failed" in message_lower:
            return {"tier": "TIER_2", "severity": "MEDIUM"}

        if "login issue" in message_lower or "redirect" in message_lower:
            return {"tier": "TIER_1", "severity": "LOW"}

        # Default classification
        return {"tier": "TIER_1", "severity": "LOW"}