# backend/agents/orchestrator.py
from backend.agents.router import IntentRouter
from backend.agents.billing import BillingAgent
from backend.agents.technical import TechnicalAgent
from backend.agents.product import ProductAgent
from backend.agents.complaint import ComplaintAgent
from backend.agents.faq import FAQAgent

class MultiAgentOrchestrator:
    def __init__(self):
        self.router = IntentRouter()
        
        # Initialize the specialized workforce mapping
        self.agent_registry = {
            "billing": BillingAgent(),
            "technical": TechnicalAgent(),
            "product": ProductAgent(),
            "complaint": ComplaintAgent(),
            "faq": FAQAgent()
        }

    def process_customer_query(self, query: str, context: str = "", history: list = None) -> dict:
        """Routes query, executes target sub-agents, and builds a comprehensive payload."""
        
        routing_decision = self.router.route_query(query)
        selected_agents = routing_decision.get("selected_agents", ["faq"])
        justification = routing_decision.get("justification", "")

        responses = {}
        
        for agent_key in selected_agents:
            agent = self.agent_registry.get(agent_key)
            if agent:
                print(f"🤖 Activating specialized: {agent.agent_name}")
                # MUST pass context=context here!
                responses[agent_key] = agent.generate_response(query, context=context)

        # 3. Aggregate answers cleanly if multiple agents were used
        if len(responses) == 1:
            final_text = list(responses.values())[0]
        else:
            final_text = "Here is the combined breakdown regarding your request:\n\n"
            for agent_key, answer in responses.items():
                section_title = agent_key.replace("_", " ").title()
                final_text += f"**[{section_title} Aspect]**\n{answer}\n\n"

        return {
            "query": query,
            "routed_agents": selected_agents,
            "justification": justification,
            "response": final_text.strip()
        }

if __name__ == "__main__":
    # Multi-agent edge-case verification test
    orchestrator = MultiAgentOrchestrator()
    sample_complex_query = "I ordered a laptop yesterday, but my card was charged twice and I never got a confirmation email!"
    
    print("🧪 Simulating Complex Multi-Agent Request...")
    output = orchestrator.process_customer_query(sample_complex_query)
    print("\n--- AGGREGATED OUTPUT payload ---")
    print(f"Agents Triggered: {output['routed_agents']}")
    print(f"Final Response Provided:\n{output['response']}")