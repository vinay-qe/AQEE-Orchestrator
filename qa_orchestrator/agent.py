from google.adk.agents import LlmAgent
from .agents import architect
from .agents import designer
from .agents import planner
from .custom_functions import validate_phase_output
from google.adk.tools import FunctionTool

# Initialize tools
validator_tool = FunctionTool(func=validate_phase_output)

# Define the Root Orchestrator
root_agent = LlmAgent(
    name="AQEE_Orchestrator",
    model="gemini-2.0-flash",
    instruction="""You are the Root Orchestrator.
    Coordinate the 7-phase QA lifecycle by delegating to sub_agents.
    Validate outputs using validate_phase_output before moving to the next phase.""",
    sub_agents=[architect, planner, designer], # Add other specialists here later
    tools=[validator_tool],
    memory=True
)