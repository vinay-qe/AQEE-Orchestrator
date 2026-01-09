# AQEE - Agent QA Engineering Ecosystem

A **production-ready multi-agent system** for automating the complete QA lifecycle using Google's Agent Development Kit (ADK), Gemini 3 Flash AI models, and Azure DevOps integration.

**Built for enterprise QA teams** | Secure credential management | 7-phase QA lifecycle automation | Real-time collaboration

---

## 🎯 What is AQEE?

AQEE is an **autonomous AI-powered QA orchestration platform** that coordinates 7 specialized agents to handle the entire quality assurance lifecycle—from requirements to reporting. Each agent is a domain expert focused on one aspect of QA.

**Transforms QA from manual, sequential work into intelligent, parallel automation.**

---

## 🤖 Agent Team (current)

AQEE now uses a modular set of specialized agents. Heavy agents have been split into focused specialists; the orchestrator composes them as needed.

Key agents (high level):
- `Requirement_Analyst`, `Story_Architect`, `AcceptanceCriteria_Manager`, `DevOps_Linker` — requirements & story creation
- `Project_Planner`, `Resource_Planner` — planning and resourcing
- `TestPlan_Designer`, `TestCase_Author`, `Coverage_Analyst`, `TestData_Engineer`, `Suite_Organizer` — test design and coverage
- `UI_Framework_Designer`, `API_Framework_Designer`, `CI_CD_Designer`, `Execution_Strategy_Designer`, `Environment_Manager` — automation & CI/CD design
- `Test_Executor`, `Issue_Tracker`, `Report_Generator` — execution, defect management and reporting

See the `agents/` folder for the full list of exported agents.

---

## ⚡ Key Features

### 🔐 Enterprise-Grade Security
- **Zero hardcoded secrets** - Environment variables only
- **Secure credential management** - `CredentialManager` prevents leaks
- **No credential logging** - Never exposed in logs or errors
- **Token validation** - Automatic credential checking
- **Safe by default** - Warnings for missing credentials

### 🤖 AI-Powered Orchestration
- **Gemini 3 Flash models** - Fast, efficient, cost-effective
- **Intelligent delegation** - Root agent routes tasks to specialists
- **Parallel execution** - Multiple agents work simultaneously
- **Context awareness** - Agents understand QA best practices
- **Adaptive responses** - Agents learn from feedback

### 🔗 Azure DevOps Integration
- **Secure API client** - Safe credential handling
- **Create artifacts** - User Stories, Test Plans, Test Cases
- **Link requirements** - Connect stories to tests
- **Track issues** - Manage defects in Azure DevOps
- **Real-time sync** - Keep Azure DevOps current

### 📈 QA Metrics & Analytics
- **Test coverage tracking** - Automated metrics
- **Defect analysis** - Severity, priority, trends
- **Effort estimation** - Data-driven planning
- **Risk assessment** - Early issue identification
- **Stakeholder dashboards** - Executive summaries

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+**
- **Google Gemini API Key** (free or paid tier)
- **Azure DevOps Personal Access Token** (optional)
- **Git** (for version control)

### 1. Setup Project

```powershell
# Clone or navigate to project
cd qa-agent-ecosystem

# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Credentials

**Option A: Environment Variables (Recommended)**
```powershell
$env:GOOGLE_API_KEY = 'your-google-api-key'
$env:AZURE_DEVOPS_TOKEN = 'your-azure-pat-token'
$env:AZURE_DEVOPS_ORG_URL = 'https://dev.azure.com/Cognitive-QE-Labs'
```

**Option B: Local .env File**
```powershell
cp .env.example .env
# Edit .env with your credentials
```

### 3. Launch AQEE

```powershell
$env:PYTHONPATH = 'C:\src\qa-agent-ecosystem'
adk web --port 8000
```

### 4. Access the UI

- Open **http://localhost:8000** in your browser
- Select **AQEE_Orchestrator** from the dropdown
- Start orchestrating QA! 🚀

---

## 🔐 Security & Credentials

### Getting Your Credentials

#### Google Gemini API Key
1. Visit https://aistudio.google.com/app/apikey
2. Create a new API key
3. For production use, enable billing on the project
4. Copy the key

#### Azure DevOps Personal Access Token
1. Go to https://dev.azure.com/{your-org}/_usersSettings/tokens
2. Click "New Token"
3. Configure scopes:
   - ✅ Work Items (Read & Write)
   - ✅ Test Management (Read & Write)
4. Create and copy the token

### Secure Credential Management

**AQEE includes `qa_orchestrator/secrets.py` which:**
- Loads credentials from environment variables
- Validates credential presence
- Never logs actual credential values
- Prevents credential leakage in errors
- Supports credential rotation

**Safe credential access:**
```python
from qa_orchestrator.secrets import get_credential, has_credential

# Check if credential exists (safe, no value exposure)
if has_credential("google_api_key"):
    api_key = get_credential("google_api_key")
    # Use api_key for API calls
```

### ⚠️ Security Best Practices

**DO:**
- ✅ Use environment variables for credentials
- ✅ Use Personal Access Tokens (not passwords)
- ✅ Keep `.env` file in `.gitignore`
- ✅ Rotate credentials every 90 days
- ✅ Use strong, complex credentials
- ✅ Review logs for credential exposure
- ✅ Revoke exposed tokens immediately

**DON'T:**
- ❌ Hardcode credentials in source code
- ❌ Commit `.env` to version control
- ❌ Share credentials via email or chat
- ❌ Log credential values
- ❌ Use weak or default credentials
- ❌ Keep exposed credentials in use
- ❌ Reuse compromised tokens

**See [SECURITY.md](SECURITY.md) for comprehensive security guidelines.**

---

## 📖 Project Structure

```
qa-agent-ecosystem/
├── agent.py                          # 🎯 Root orchestrator (main entry point)
├── test_agents.py                    # 🧪 Agent verification script
├── requirements.txt                  # 📦 Python dependencies
├── pyproject.toml                    # 📋 Package configuration
├── .env.example                      # 🔑 Credential template
├── SECURITY.md                       # 🔒 Security guidelines
├── README.md                         # 📖 This file
│
├── agents/                           # 👥 Specialized agent team
│   ├── architect.py                  # Legacy architect (compatibility)
│   ├── requirement_analyst.py        # Requirement extraction & clarification
│   ├── story_architect.py            # Story construction and templates
│   ├── acceptance_criteria_manager.py# BDD criteria validation/normalization
│   ├── devops_linker.py              # Azure DevOps payload/link suggestions
│   ├── planner.py                    # Project planning
│   ├── resource_planner.py           # Resource planning
│   ├── testplan_designer.py          # High-level test plan authoring
│   ├── testcase_author.py            # Test case authoring from GWT
│   ├── coverage_analyst.py           # Coverage mapping & gap analysis
│   ├── testdata_engineer.py          # Test data factories & fixtures
│   ├── suite_organizer.py            # Suite grouping and CI mapping
│   ├── test_automation_designer.py   # Legacy automation designer (compat)
│   ├── ui_framework_designer.py      # UI automation framework design
│   ├── api_framework_designer.py     # API automation framework design
│   ├── ci_cd_designer.py             # CI/CD pipeline templates
│   ├── execution_strategy_designer.py# Execution cadence and flakiness policy
│   ├── environment_manager.py        # Environment provisioning & secrets
│   ├── designer.py                   # Compatibility wrapper for test design
│   ├── test_executor.py              # Test execution orchestrator
│   ├── report_generator.py           # Reporting
│   ├── issue_tracker.py              # Defect tracking
│   └── __init__.py                   # Module initialization (exports)
│
└── qa_orchestrator/                  # 🛠️ Core utilities
    ├── agent.py                      # Legacy agent definitions
    ├── secrets.py                    # 🔐 Secure credential handling
    ├── azure_devops.py               # 🔗 Azure DevOps client
    ├── custom_functions.py           # ⚙️ Validation tools
    ├── .env                          # 🔑 Local credentials (NEVER commit)
    ├── __pycache__/                  # Python cache
    └── .adk/                         # ADK artifacts directory
```

---

## 🎓 Usage Examples

### Example 1: Simple Test Planning
```
User: "I need comprehensive tests for a login form"

AQEE orchestrates:
1. 🏗️ Architect → Creates user stories for login feature
2. 📋 Planner → Creates test plan with timeline
3. ✅ Designer → Designs 25+ test cases (positive, negative, edge cases)
4. 📊 Reporter → Generates test coverage report
```

### Example 2: Full QA Cycle with Azure DevOps
```
User: "Automate QA for the payment module in Azure DevOps"

AQEE orchestrates:
1. 🏗️ Architect → Creates user stories in Azure DevOps
2. 📋 Planner → Creates test plan in Azure DevOps
3. ✅ Designer → Creates test cases linked to stories
4. 🧪 Executor → Runs tests and records results
5. 🐛 Tracker → Creates defects in Azure DevOps
6. 📊 Reporter → Generates executive dashboard
7. 📈 Planner → Estimates effort for next sprint
```

### Example 3: Defect Triage & Analysis
```
User: "Analyze and prioritize the 47 failing tests"

AQEE orchestrates:
1. 🧪 Executor → Re-runs tests with detailed logging
2. 🐛 Tracker → Triages failures by severity & impact
3. 📊 Reporter → Creates defect trend analysis
4. 📈 Planner → Estimates fix effort & resources
```

---

## 🔧 Agent Capabilities

### Requirement_Architect
- Analyzes business requirements
- Creates user stories with acceptance criteria
- Breaks down epics into manageable stories
- Creates stories in Azure DevOps
- Output: Well-structured, testable requirements

### Project_Planner
- Creates comprehensive test plans
- Estimates QA effort and resources
- Defines testing timeline and milestones
- Plans test coverage strategy
- Creates test plans in Azure DevOps
- Output: Actionable, resourced test plans

### TestCase_Designer
- Designs positive, negative, edge case tests
- Creates test cases with clear steps
- Optimizes for maintainability
- Links tests to requirements
- Creates test cases in Azure DevOps
- Output: Comprehensive, maintainable test suites

### Test_Executor
- Executes manual and automated tests
- Records detailed results
- Captures logs and environment info
- Identifies flaky tests
- Tracks execution metrics
- Output: Detailed execution reports with metrics

### Issue_Tracker
- Creates detailed defect reports
- Triages issues by severity & priority
- Tracks issue lifecycle
- Links issues to test cases
- Creates issues in Azure DevOps
- Output: Prioritized, organized issue backlog

### Report_Generator
- Creates test execution reports
- Generates defect trend analysis
- Produces stakeholder dashboards
- Calculates QA metrics (pass rate, coverage)
- Documents lessons learned
- Output: Executive-ready QA reports

### Resource_Planner
- Estimates QA effort and cost
- Plans team allocation
- Optimizes test execution schedules
- Prioritizes automation opportunities
- Forecasts timelines
- Output: Data-driven resource plans

---

## 📊 Architecture

```
┌─────────────────────────────────────────────┐
│           AQEE_Orchestrator (Root)          │
│    Intelligent QA Lifecycle Coordinator     │
└──────────────┬──────────────────────────────┘
               │
    ┌──────────┼──────────┬─────────┬──────────┐
    │          │          │         │          │
    ▼          ▼          ▼         ▼          ▼
  Phase 1    Phase 2    Phase 3   Phase 4   Phase 5
 Architect   Planner   Designer  Executor  Tracker
    │          │          │         │          │
    └──────────┴──────────┴─────────┴──────────┘
               │
    ┌──────────┴──────────┐
    │                     │
    ▼                     ▼
 Phase 6               Phase 7
Reporter            Planner
 (Reports)         (Optimization)

All agents ← Azure DevOps Integration
All agents ← Gemini 3 Flash AI Models
```

---

## 🧪 Testing & Validation

### Run Agent Verification
```powershell
.venv\Scripts\python.exe test_agents.py
```

Expected output:
```
Expected output (example):
```
Missing credentials: google_api_key, azure_devops_token, azure_devops_org_url
✓ Root agent loaded: AQEE_Orchestrator
✓ Model: gemini-3-flash
✓ Sub-agents count: 22
✓ Sub-agents:
    - Requirement_Analyst
    - Story_Architect
    - AcceptanceCriteria_Manager
    - DevOps_Linker
    - TestPlan_Designer
    - TestCase_Author
    - Coverage_Analyst
    - TestData_Engineer
    - Suite_Organizer
    - UI_Framework_Designer
    - API_Framework_Designer
    - CI_CD_Designer
    - Execution_Strategy_Designer
    - Environment_Manager
    - Project_Planner
    - TestCase_Designer (compat)
    - Test_Automation_Designer (compat)
    - Test_Executor
    - Report_Generator
    - Issue_Tracker
    - Resource_Planner
✓ Tools count: 1

✅ All agents loaded successfully!
```

---

## 🚨 Troubleshooting

### Issue: "429 RESOURCE_EXHAUSTED"
**Problem:** Free-tier Gemini quota exceeded
**Solution:** 
- Enable billing on your Google Cloud project
- Or wait for quota reset (next day)
- Check quota at: https://ai.dev/rate-limit

### Issue: Azure DevOps integration not working
**Problem:** Token or org URL missing/invalid
**Solution:**
```powershell
# Verify credentials are set
$env:AZURE_DEVOPS_TOKEN
$env:AZURE_DEVOPS_ORG_URL

# Regenerate token if needed
# Go to: https://dev.azure.com/{org}/_usersSettings/tokens
```

### Issue: "No module named 'agent'"
**Problem:** PYTHONPATH not set
**Solution:**
```powershell
$env:PYTHONPATH = 'C:\src\qa-agent-ecosystem'
adk web
```

---

## 🔄 Continuous Improvement

AQEE learns and improves through:
- **Metrics tracking** - What worked, what didn't
- **Pattern recognition** - AI identifies QA trends

---

## 🆕 Recent changes

- Split large agents into smaller, focused specialists (architect, designer, test_automation_designer).
- Added compatibility wrappers `designer.py` and `architect.py` that delegate to specialized agents and aggregate outputs.
- Wired compatibility wrappers to use the ADK `agent.call(prompt, context)` signature with safe fallbacks.
- Added unit tests for credential management and Azure DevOps client in `tests/`.
- Updated project exports and root orchestrator to register all new agents.

For full details, see commit history and the `AGENT_ENHANCEMENTS.md` and `DESIGNER_EDGE_CASES.md` documents.
- **Feedback loops** - Integration with team insights
- **Process optimization** - Agent recommendations
- **Cost analysis** - Automation ROI tracking

---

## 🤝 Extend AQEE

### Add Custom Agents
```python
# Create agents/my_agent.py
from google.adk.agents import LlmAgent

my_agent = LlmAgent(
    name="My_Specialist",
    model="gemini-3-flash",
    description="Does something specific",
    instruction="Your detailed instructions here"
)
```

### Add Custom Tools
```python
# Create qa_orchestrator/my_tools.py
from google.adk.tools import FunctionTool

def my_function(param1: str) -> dict:
    """My custom tool function."""
    return {"result": "something"}

my_tool = FunctionTool(func=my_function)

# Add to root_agent.tools
```

### Integrate Other Services
See `qa_orchestrator/azure_devops.py` for integration pattern:
- Load credentials safely
- Create client class
- Implement API methods
- Handle errors gracefully
- Never expose credentials

---

## 📚 Documentation

- **[SECURITY.md](SECURITY.md)** - Complete security guidelines
- **[Google ADK Docs](https://google.github.io/adk-docs/)** - ADK documentation
- **[Azure DevOps API](https://learn.microsoft.com/en-us/rest/api/azure/devops/)** - Azure API reference
- **[Gemini API](https://ai.google.dev)** - Google AI documentation

---

## 📝 License

AQEE is an educational project for QA automation demonstration.

---

## 🎉 Ready to Transform Your QA?

1. **Rotate exposed token** (see Security section above)
2. **Get credentials** (Google API Key + Azure PAT)
3. **Configure credentials** (environment or .env)
4. **Launch AQEE** (`adk web --port 8000`)
5. **Start orchestrating** - Let the agents handle QA!

**Questions? Check [SECURITY.md](SECURITY.md) for detailed guidance.**

---

**Made with ❤️ for Quality Assurance Teams** | Built on Google ADK | Powered by Gemini 3 Flash | Integrated with Azure DevOps
