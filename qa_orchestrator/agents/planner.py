
from google.adk.agents import LlmAgent

planner = LlmAgent(
    name="Project_Planner",
    model="gemini-2.0-flash",
    description="Plans project roadmap and resource allocation based on User Stories.",
    instruction="""Take User Stories from the Architect.
    1. Prioritize stories.
    2. Create a project roadmap with timelines.
    3. Estimate resources needed.
    4. Create Test Plan.
    Output: JSON roadmap and resource plan.""",
    output_key="phase2_data"
)