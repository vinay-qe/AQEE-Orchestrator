from google.adk.agents import LlmAgent

testplan_designer = LlmAgent(
    name="TestPlan_Designer",
    model="gemini-3-flash",
    description="Creates high-level test plans, scope, milestones and resources mapping for a feature.",
    instruction="""You are the Test Plan Designer.

Responsibilities:
- Create test plan name, scope, phases, milestones and resource needs
- Map user stories to test phases and identify success criteria

Output JSON:
{
  "name": "...",
  "scope": ["story_ids"],
  "phases": ["Functional","Regression"],
  "milestones": [{"name":"...","date":"..."}]
}
""",
)
