from google.adk.agents import LlmAgent

# Compatibility wrapper: the heavy `TestCase_Designer` responsibilities have
# been split into focused agents: TestPlan_Designer, TestCase_Author,
# Coverage_Analyst, TestData_Engineer, and Suite_Organizer. This agent
# remains available for backward compatibility and high-level orchestration.
designer = LlmAgent(
    name="TestCase_Designer",
    model="gemini-3-flash",
    description=(
        "Compatibility wrapper that orchestrates test-plan, test-case, "
        "coverage and test-data specialists. Prefer using the specialized "
        "agents directly for fine-grained control."
    ),
    instruction="""You are the (compatibility) TestCase Designer.

Behavior and delegation rules:
- For high-level test planning requests, delegate to `TestPlan_Designer`.
- To author executable test cases from Given-When-Then criteria, call `TestCase_Author`.
- For coverage metrics and gap analysis, call `Coverage_Analyst`.
- For test data factories, mocking and fixtures, call `TestData_Engineer`.
- For suite organization and CI mapping, call `Suite_Organizer`.

Compatibility outputs:
- When asked for a monolithic test design output, aggregate the outputs from
  the specialised agents into the legacy JSON schema so existing consumers
  remain compatible.

Advice to users:
- New integrations should call the specialized agents directly.
- Use this wrapper only when you need a single, backward-compatible response
  from the older `TestCase_Designer` interface.

Output format: Preserve existing `phase3_data` schema for compatibility.
""",
    output_key="phase3_data",
)


def _call_agent(agent, payload):
  """Call agent using preferred ADK signature `call(prompt, context)` then fall back.

  We form a short prompt from the payload and pass payload as context.
  """
  # Preferred explicit ADK signature
  call_fn = getattr(agent, "call", None)
  if callable(call_fn):
    try:
      prompt = payload.get("prompt") if isinstance(payload, dict) else str(payload)
      return call_fn(prompt, payload)
    except Exception as e:
      return {"error": f"agent.call failed: {e}"}

  # Fallback to other common methods
  for method in ("run", "invoke", "execute", "respond", "get_response"):
    fn = getattr(agent, method, None)
    if callable(fn):
      try:
        return fn(payload)
      except Exception as e:
        return {"error": f"agent {method} failed: {e}"}

  # Final fallback: placeholder
  return {
    "agent": getattr(agent, "name", str(agent)),
    "note": "no callable method available; returned placeholder",
    "instruction": getattr(agent, "instruction", None),
    "input_received": payload,
  }


def delegate_design(input_data: dict) -> dict:
  """Delegate design tasks to specialized designer agents and aggregate outputs.

  Args:
    input_data: dict containing stories/acceptance criteria and context

  Returns:
    Aggregated dict following legacy `phase3_data` shape as best-effort.
  """
  from agents.testplan_designer import testplan_designer
  from agents.testcase_author import testcase_author
  from agents.coverage_analyst import coverage_analyst
  from agents.testdata_engineer import testdata_engineer
  from agents.suite_organizer import suite_organizer

  agg = {}

  # Call each specialized agent with the provided input and collect results
  agg["test_plan"] = _call_agent(testplan_designer, input_data)
  agg["test_cases"] = _call_agent(testcase_author, input_data)
  agg["coverage_analysis"] = _call_agent(coverage_analyst, input_data)
  agg["test_data"] = _call_agent(testdata_engineer, input_data)
  agg["suites"] = _call_agent(suite_organizer, input_data)

  # Normalize into legacy fields where possible
  result = {
    "story_status": "ACCEPTED",
    "acceptance_criteria_status": "VALID",
    "test_plan": agg.get("test_plan"),
    "test_suites": agg.get("suites"),
    "test_cases": agg.get("test_cases"),
    "coverage_analysis": agg.get("coverage_analysis"),
    "test_data": agg.get("test_data"),
    "clarification_questions": [],
    "validation_errors": [],
  }

  # If any agent returned an error, record it
  for k, v in agg.items():
    if isinstance(v, dict) and v.get("error"):
      result["validation_errors"].append(f"{k}: {v.get('error')}")

  return result