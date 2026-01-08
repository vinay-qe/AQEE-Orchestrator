from google.adk.agents import LlmAgent

architect = LlmAgent(
    name="Requirement_Architect",
    model="gemini-2.0-flash",
    description="Analyzes input requirements and creates detailed User Stories in Azure DevOps.",
    instruction="""Analyze input requirements. 
    1. Identify key features. 
    2. Create User Stories in Azure DevOps.
    3. Add acceptance criteria.
    Output: JSON mapping of stories to features.""",
    output_key="phase1_data"
)