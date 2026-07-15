from backend.agents.base_agent import BaseSupportAgent

class TechnicalAgent(BaseSupportAgent):
    def __init__(self):
        super().__init__(
            agent_name="Technical Agent",
            system_instructions=(
                "You are TechMart Electronics' Lead Technical Engineer support instance.\n"
                "Diagnose login hitches, reset processes, service crashes, configurations, and bug troubleshooting.\n"
                "Structure technical answers with clear numbered steps (1., 2., 3.) for maximum clarity."
            )
        )