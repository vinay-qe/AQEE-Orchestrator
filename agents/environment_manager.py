from google.adk.agents import LlmAgent

environment_manager = LlmAgent(
    name="Environment_Manager",
    model="gemini-3-flash",
    description="Designs environment provisioning, test data isolation, credentials handling and infrastructure needs.",
    instruction="""You are the Environment Manager.

Responsibilities:
- Recommend environment tiers (dev/stage/prod), provisioning options (containers, cloud), and secrets handling
- Suggest test data isolation and cleanup approaches

Output JSON:
{
  "environments": ["dev","staging","prod"],
  "provisioning": "docker-compose/k8s/managed",
  "secrets_handling": "env/vault"
}
""",
)
