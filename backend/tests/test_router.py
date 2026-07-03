from services.llm_router import AgentRouter
from services.prompts import ROUTER_PROMPT, SALES_AGENT_PROMPT, CLAIMS_AGENT_PROMPT
from database import CallOutcome


def test_router_starts_in_router_mode():
    router = AgentRouter(call_sid="test_sid_123")
    assert router.current_mode == "router"


def test_router_seeds_system_prompt():
    router = AgentRouter(call_sid="test_sid_123")
    assert router.conversation_history[0]["role"] == "system"
    assert router.conversation_history[0]["content"] == ROUTER_PROMPT


def test_prompts_demand_json_output():
    # every agent prompt must force the json contract the router parses
    for prompt in (ROUTER_PROMPT, SALES_AGENT_PROMPT, CLAIMS_AGENT_PROMPT):
        assert "JSON" in prompt
        assert '"message"' in prompt


def test_call_outcomes_cover_triggers():
    # the trigger -> outcome mapping in llm_router depends on these enum members existing
    for member in ("SALE_CLOSED", "REJECTED_OTHER", "ESCALATED_LEGAL_RISK", "ESCALATED_HUMAN"):
        assert hasattr(CallOutcome, member)
