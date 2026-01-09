# AQEE - Agent QA Engineering Ecosystem

A multi-agent system for automating the complete QA lifecycle using Google's ADK and Azure DevOps integration.

## 🔐 Security & Credential Management

### Best Practices for Handling API Keys

**Never expose credentials in:**
- Source code or version control
- Logs or debug output
- Error messages or UI displays
- Configuration files committed to git
- Environment files without `.gitignore`

### Secure Setup

1. **Use Environment Variables (Recommended)**
   ```powershell
   $env:GOOGLE_API_KEY = 'your-api-key-here'
   $env:AZURE_DEVOPS_TOKEN = 'your-pat-token-here'
   $env:AZURE_DEVOPS_ORG_URL = 'https://dev.azure.com/yourorg'
   ```

2. **Local `.env` File (Development Only)**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` with your actual credentials
   - **NEVER** commit `.env` to git (it's in `.gitignore`)
   - Each developer has their own local `.env`

3. **Secrets Module**
   The project includes `qa_orchestrator/secrets.py` that:
   - Loads credentials safely from environment
   - Never logs actual credential values
   - Validates credential presence
   - Supports credential rotation

### Getting Your Credentials

#### Google API Key
1. Go to https://aistudio.google.com/app/apikey
2. Create a new API key
3. Enable billing on the project for production use
4. Set as environment variable: `GOOGLE_API_KEY`

#### Azure DevOps
1. Go to https://dev.azure.com/{your-org}/_usersSettings/tokens
2. Create a Personal Access Token (PAT) with these scopes:
   - Work Items (Read & Write)
   - Test Management (Read & Write)
3. Set as environment variables:
   - `AZURE_DEVOPS_TOKEN` - Your PAT
   - `AZURE_DEVOPS_ORG_URL` - https://dev.azure.com/yourorg

### Using Credentials in Code

```python
from qa_orchestrator.secrets import get_credential, has_credential

# Check if credential exists (safe, doesn't expose value)
if has_credential("google_api_key"):
    api_key = get_credential("google_api_key")
    # Use api_key for API calls
```

### Credential Validation

The `CredentialManager` class automatically:
- Loads from environment on first access
- Validates presence of required credentials
- Logs warnings for missing optional credentials
- Never exposes actual values in logs or errors

### For CI/CD Pipelines

Store secrets in your CI/CD platform:
- **GitHub**: GitHub Secrets → Set environment variables
- **Azure Pipelines**: Pipeline secrets → Pass as variables
- **GitLab**: CI/CD Variables → Set as masked variables

Never hardcode or commit credentials to any branch!

---

## 📊 AQEE Agents

### 7-Phase QA Lifecycle

The system includes 7 specialized agents:

1. **Requirement_Architect** - Requirements → User Stories
2. **Project_Planner** - Planning → Resource Allocation
3. **TestCase_Designer** - User Stories → Test Cases
4. **Test_Executor** - Executes tests → Captures Results
5. **Issue_Tracker** - Manages defects → Tracks Issues
6. **Report_Generator** - Creates reports → Dashboards
7. **Resource_Planner** - Estimates effort → Optimizes schedules

### Azure DevOps Integration

The `qa_orchestrator/azure_devops.py` module provides:
- Create User Stories with acceptance criteria
- Create Test Plans and Test Cases
- Link work items to requirements
- Retrieve project information

All methods safely handle credentials and log errors without exposing sensitive data.

---

## 🚀 Quick Start

### Setup

```powershell
# 1. Activate virtual environment
.venv\Scripts\Activate.ps1

# 2. Set up credentials (choose one method)
# Option A: Environment variables
$env:GOOGLE_API_KEY = 'your-key'
$env:AZURE_DEVOPS_TOKEN = 'your-token'
$env:AZURE_DEVOPS_ORG_URL = 'your-url'

# Option B: Local .env file
cp .env.example .env
# Edit .env with your credentials

# 3. Set Python path and start ADK web
$env:PYTHONPATH = 'C:\src\qa-agent-ecosystem'
adk web --port 8000
```

### Access
Open http://localhost:8000 in your browser

---

## 📁 Project Structure

```
qa-agent-ecosystem/
├── agent.py                    # Root orchestrator (ADK discovery)
├── .env.example                # Template for credentials
├── pyproject.toml              # Package metadata
├── agents/
│   ├── architect.py            # Requirement analysis
│   ├── planner.py              # Project planning
│   ├── designer.py             # Test case design
│   ├── test_executor.py        # Test execution
│   ├── report_generator.py     # Report generation
│   ├── issue_tracker.py        # Issue management
│   └── resource_planner.py     # Resource planning
└── qa_orchestrator/
    ├── secrets.py              # Secure credential management
    ├── azure_devops.py         # Azure DevOps integration
    ├── custom_functions.py     # Validation tools
    └── .env                    # Local credentials (NEVER commit)
```

---

## 🔒 Security Checklist

- [ ] Never commit `.env` file to git
- [ ] Use unique API keys per environment
- [ ] Rotate credentials regularly
- [ ] Use Personal Access Tokens (not passwords) for Azure
- [ ] Review logs for credential leakage
- [ ] Use strong, complex credentials
- [ ] Restrict credential permissions (least privilege)
- [ ] Monitor credential usage and access

---

## 📖 Additional Resources

- [Google Gemini API Docs](https://ai.google.dev)
- [Azure DevOps REST API](https://learn.microsoft.com/en-us/rest/api/azure/devops)
- [ADK Python Documentation](https://google.github.io/adk-docs/get-started/python/)

---

## 📝 License

AQEE is an educational project for QA automation.
