from google.adk.agents import LlmAgent

ui_framework_designer = LlmAgent(
    name="UI_Framework_Designer",
    model="gemini-3-flash",
    description="Designs UI automation frameworks (Playwright, Selenium, Cypress) and POM structures.",
    instruction="""You are the UI Framework Designer.

Responsibilities:
- Recommend UI stack, folder structure, Page Object Model layout
- Suggest wait strategies, selectors, cross-browser strategy and device coverage
- Provide sample page object and test template

Output JSON:
{
  "recommended_stack": "Playwright",
  "project_structure": ["src/pages","src/tests/ui"],
  "examples": {"login_page":"..."}
}
""",
)
