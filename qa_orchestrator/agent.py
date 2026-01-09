from google.adk.agents import LlmAgent

# Lightweight root agent for ADK discovery. Keep construction minimal to avoid
# any network or heavy import side-effects at module import time.
root_agent = LlmAgent(
    name="AQEE_Orchestrator",
    model="gemini-2.0-flash",
    description="Root orchestrator that coordinates the 7-phase QA lifecycle",
    instruction="""You are the Root Orchestrator.
    Coordinate the 7-phase QA lifecycle by delegating to sub-agents.
    Handle the complete QA lifecycle across multiple phases."""
)


def init_runtime_components():
    """Attach tools and sub-agents to `root_agent` at runtime.

    Call this from your runtime entrypoint (or before running the agent) so
    that imports which may call external services are delayed until needed.
    """
    # Avoid re-initializing
    if getattr(root_agent, "_runtime_initialized", False):
        return

    # Local imports to prevent import-time side-effects
    from google.adk.tools import FunctionTool
    from .custom_functions import validate_phase_output

    # Import agent instances lazily (these modules should only define agents)
    try:
        from agents.architect import architect
        from agents.planner import planner
        from agents.designer import designer
    except Exception:
        # If sub-agents aren't importable, leave sub_agents empty; caller can
        # handle/report the error when attempting to run.
        architect = planner = designer = None

    # Initialize tools lazily
    validator_tool = FunctionTool(func=validate_phase_output)

    sub_agents = [a for a in (architect, planner, designer) if a is not None]

    # Attach to root_agent
    if sub_agents:
        setattr(root_agent, "sub_agents", sub_agents)
    setattr(root_agent, "tools", [validator_tool])
    setattr(root_agent, "_runtime_initialized", True)


def ensure_runtime_initialized():
    """Helper that initializes runtime components and raises a helpful error
    if initialization failed due to import errors.
    """
    try:
        init_runtime_components()
    except Exception as e:
        raise RuntimeError("Failed to initialize runtime components for root_agent") from e
