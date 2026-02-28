class IntentState:
    """
    Represents the state of an email generation intent.
    Tracks selections through the domain > recipient > category > scenario hierarchy.
    """

    def __init__(self):
        """Initialize an empty intent state."""
        self.domain = None
        self.recipient = None
        self.category = None
        self.scenario = None
        self.scenario_meta = {}

    def summary(self):
        """
        Get a human-readable summary of the current intent path.

        Returns:
            str: Intent path in format "Domain → Recipient → Category → Scenario"
        """
        parts = [
            self.domain,
            self.recipient,
            self.category,
            self.scenario
        ]
        return " → ".join([p for p in parts if p])

    def is_complete(self):
        """
        Check if all required selections have been made.

        Returns:
            bool: True if all fields are selected
        """
        return all([self.domain, self.recipient, self.category, self.scenario])

    def to_dict(self):
        """
        Convert state to dictionary representation.

        Returns:
            dict: State as dictionary
        """
        return {
            "domain": self.domain,
            "recipient": self.recipient,
            "category": self.category,
            "scenario": self.scenario,
            "meta": self.scenario_meta
        }