🌟 AQEE-Orchestrator: AI-Driven Quality Engineering Ecosystem
AQEE (AI-Driven Quality Engineering Ecosystem) is an autonomous multi-agent platform built with the Google Agent Development Kit (ADK) and Gemini 2.0. It automates the 7-phase QA lifecycle, from requirement analysis to ROI reporting.


## 🏗️ Project Architecture
- **Orchestrator:** A central manager (LlmAgent) that handles state, validation, and reporting.
- **Specialists:** Modular agents (Architect, Designer, Automator) focused on specific QA phases.
- **Tools:** Custom Python functions and MCP (Model Context Protocol) for Azure DevOps integration.
.

🏗️ Workflow Architecture
The system uses a Manager-Worker pattern. The Root Orchestrator (Manager) coordinates specialized agents (Workers) and validates their output using custom Python tools.

Code snippet

graph TD
    User((User)) -->|Input Requirements| Root[Root Orchestrator]
    Root -->|Phase 1| Arch[Requirement Architect]
    Arch -->|JSON Output| Val{Validator Tool}
    Val -->|Invalid| Arch
    Val -->|Valid| Root
    Root -->|Phase 2| Plan[Test Strategist]
    Root -->|Phase 3| Design[Test Designer]
    Design -->|Report| User

🛠️ Step-by-Step Setup Guide
1. Prerequisites & Environment
Ensure you have Python 3.10 or later installed.

Bash

# 1. Clone the repository
git clone https://github.com/vinay-qe/AQEE-Orchestrator.git
cd AQEE-Orchestrator

# 2. Create a virtual environment
python -m venv .venv

# 3. Activate the environment

# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# 4. Install dependencies
pip install google-adk playwright
playwright install

2. Azure DevOps (ADO) Configuration
The agents interact with ADO to create User Stories and Test Plans.

Create Organization: Sign in to Azure DevOps and create a new organization (e.g., AQEE-Org).

Create Project: Create a new Private project named AQEE-Core.

Generate PAT: - Go to User Settings > Personal Access Tokens.

Create a new token with Work Items (Read/Write) and Test Management scopes.

Important: Save this token safely.

3. Environment Variables (.env)
Create a .env file in the root directory. Never commit this file to GitHub.

Code snippet

GOOGLE_API_KEY=your_gemini_api_key
ADO_PAT=your_azure_devops_pat
ADO_ORG=https://dev.azure.com/your-org-name
ADO_PROJECT=AQEE-Core
📁 Project Structure
The project is modular for high maintainability.

Plaintext

/AQEE-Orchestrator
├── .env                  # Private secrets (ignored by Git)
├── .gitignore            # Tells Git to ignore .env and .venv
├── README.md             # This file
├── qa_orchestrator/      # Core Package
│   ├── __init__.py       # Exposes the root_agent
│   ├── agent.py          # THE ROOT ORCHESTRATOR (Manager)
│   ├── custom_functions.py # Python Tools (Validators, Parsers)
│   └── agents/           # Specialized Workers
│       ├── __init__.py
│       ├── architect.py  # Phase 1: Requirements
│       ├── planner.py    # Phase 2: Strategy
│       └── designer.py   # Phase 3: Test Design

🚀 How to Run
You can interact with the ecosystem via the built-in ADK Web UI.

Open your terminal in the root folder.

Run the following command:

Bash

adk web qa_orchestrator
Open the URL provided (usually http://localhost:8000).

Try this prompt: "Analyze the following requirement: 'As a user, I want to be able to reset my password via email' and create the necessary stories in ADO."

🛡️ Security Note
If you accidentally push secrets to GitHub:

Revoke the token immediately in Azure DevOps.

Use git rm --cached .env and git commit --amend to scrub the history.

Update your .gitignore to include .env.