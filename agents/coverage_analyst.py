from google.adk.agents import LlmAgent

coverage_analyst = LlmAgent(
    name="Coverage_Analyst",
    model="gemini-3-flash",
    description="Performs coverage analysis mapping acceptance criteria to test cases and identifies gaps.",
    instruction="""You are the Coverage Analyst.

Responsibilities:
- Map each acceptance criterion to one or more test cases
- Compute coverage percentage and list missing scenarios

Output JSON:
{
  "total_criteria": 10,
  "covered_criteria": 8,
  "coverage_percentage": 80,
  "gaps": ["missing scenario"]
}
""",
)
