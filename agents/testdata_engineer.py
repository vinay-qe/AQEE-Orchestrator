from google.adk.agents import LlmAgent

testdata_engineer = LlmAgent(
    name="TestData_Engineer",
    model="gemini-3-flash",
    description="Designs test data factories, mocks and fixtures required for reliable test execution.",
    instruction="""You are the Test Data Engineer.

Responsibilities:
- Recommend data factories and mock strategies
- Provide sample test data and cleanup strategies

Output JSON:
{
  "factories": ["UserFactory","OrderFactory"],
  "sample_data": {"user":{"username":"testuser"}}
}
""",
)
