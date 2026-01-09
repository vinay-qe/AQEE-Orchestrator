from google.adk.agents import LlmAgent

testcase_author = LlmAgent(
    name="TestCase_Author",
    model="gemini-3-flash",
    description="Writes atomic, high-quality test cases from Given-When-Then acceptance criteria.",
    instruction="""You are the Test Case Author.

Responsibilities:
- Create test cases with ID, steps, expected results, priority and tags
- Ensure each acceptance criterion has corresponding positive and negative tests

Output JSON sample:
{
  "test_cases": [ {"id":"TC-...","title":"...","steps":["..."],"expected_results":["..."]} ]
}
""",
)
