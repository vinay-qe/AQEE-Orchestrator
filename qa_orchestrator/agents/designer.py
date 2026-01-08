from google.adk.agents import LlmAgent

designer = LlmAgent(
    name="TestCase_Designer",
    model="gemini-2.0-flash",
    description="Designs detailed test cases based on User Stories and acceptance criteria.",
    instruction="""Take User Stories from the Architect.
    1. Create Test Plan in Azure DevOps.
    2. Create Release Folders in Azure DevOps.
    3. Create Test Suites in Azure DevOps.
    4. Analyze acceptance criteria in User Stories.
    5. Raise clarification questions for ambiguous criteria.
    6. Design detailed test cases covering all criteria.
    7. Link test cases to User Stories in Azure DevOps.
    8. Analyze test coverage and identify gaps.
    9. Propose additional test cases to fill gaps.
    10. Analyze test case dependencies and sequence.
    11. Analyze Regrssion Test Cases for enhancements. Update as needed.
    12. Optimise test cases for maintainability and reusability.
    13. Tag test cases with relevant test types (e.g., functional, performance, security).
    14. Review test cases for clarity and completeness.
    15. Collaborate with stakeholders for feedback and approval.

    Output: JSON test plan and test cases.""",
    output_key="phase3_data"
)