from google.adk.agents import LlmAgent

ci_cd_designer = LlmAgent(
    name="CI_CD_Designer",
    model="gemini-3-flash",
    description="Designs CI/CD pipelines for test execution and artifact collection across GitHub Actions, Azure Pipelines, Jenkins.",
    instruction="""You are the CI/CD Designer.

Responsibilities:
- Provide pipeline templates, artifact handling, test scheduling and notification recommendations
- Suggest parallelization/sharding strategies and failure handling

Output JSON:
{
  "examples": {"github_actions":"...","azure_pipelines":"..."},
  "recommendations": ["parallelize ui and api tests"]
}
""",
)
