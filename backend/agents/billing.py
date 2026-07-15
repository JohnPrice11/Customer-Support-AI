from backend.agents.base_agent import BaseSupportAgent

class BillingAgent(BaseSupportAgent):
    def __init__(self):
        super().__init__(
            agent_name="Billing Agent",
            system_instructions=(
                "You are TechMart Electronics' Expert Billing Assistant.\n"
                "Your role is handling payments, refunds, processing invoices, or tier upgrades.\n"
                "Be meticulous, reassuring, and precise regarding numbers, dates, and clear procedural steps."
            )
        )