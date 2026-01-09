from google.adk.agents import LlmAgent

suite_organizer = LlmAgent(
    name="Suite_Organizer",
    model="gemini-3-flash",
    description="Organizes test suites, groups test cases into running suites and maps suites to CI jobs.",
    instruction="""You are the Suite Organizer.

Responsibilities:
- Group test cases into suites (smoke, regression, e2e) and map to CI jobs
- Suggest parallelization and test sharding strategy

Output JSON:
{
  "suites": [{"name":"Smoke","test_count":10}],
  "ci_mapping": {"smoke":"job-smoke"}
}
""",
)
