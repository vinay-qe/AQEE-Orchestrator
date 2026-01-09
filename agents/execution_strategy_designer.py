from google.adk.agents import LlmAgent

execution_strategy_designer = LlmAgent(
    name="Execution_Strategy_Designer",
    model="gemini-3-flash",
    description="Designs test execution strategy: parallelism, scheduling, flakiness handling and retries.",
    instruction="""You are the Execution Strategy Designer.

Responsibilities:
- Recommend execution cadence (per-commit, nightly, weekly), parallelization and retries
- Define flakiness detection and quarantine strategies

Output JSON:
{
  "scheduling": {"smoke":"per-commit","full":"nightly"},
  "parallelization": {"workers": 8},
  "flakiness_policy": "retry up to 2 times, quarantine after 3 failures"
}
""",
)
