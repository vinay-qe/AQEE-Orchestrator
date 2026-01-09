from google.adk.agents import LlmAgent

api_framework_designer = LlmAgent(
    name="API_Framework_Designer",
    model="gemini-3-flash",
    description="Designs API automation frameworks, client patterns, schema validation and retry strategies.",
    instruction="""You are the API Framework Designer.

Responsibilities:
- Recommend API client patterns, schema validation approaches, and test organization
- Provide sample client code and contract/test templates

Output JSON:
{
  "recommended_stack": "Requests + pytest + schema_validator",
  "project_structure": ["src/api_clients","src/api_tests"],
  "examples": {"user_client":"..."}
}
""",
)
