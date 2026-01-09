# AQEE Setup Guide - Complete Configuration Instructions

This guide walks you through setting up AQEE with your Azure DevOps and Google Gemini credentials.

## ⚠️ URGENT: Token Security Issue

**Your Azure DevOps Personal Access Token was exposed in conversation history.**

### Immediate Action Required

1. **Revoke the exposed token immediately:**
   ```
   Go to: https://dev.azure.com/Cognitive-QE-Labs/_usersSettings/tokens
   ```
   - Find the token that was exposed
   - Click "..." → "Revoke"
   - Confirm revocation
   - **This is CRITICAL - Do NOT skip this step**

2. **Create a new Personal Access Token:**
   ```
   Go to: https://dev.azure.com/Cognitive-QE-Labs/_usersSettings/tokens
   ```
   - Click "+ New Token"
   - Name: `AQEE-Production` (or your preference)
   - Organization: Select "Cognitive-QE-Labs"
   - Expiration: 90 days (recommended for security)
   - Scopes (check these exactly):
     - ✅ Work Items (Read & Write)
     - ✅ Test Management (Read & Write)
   - Click "Create"
   - **Copy the token immediately** - you won't see it again

---

## 📋 Your Azure DevOps Information

Based on your configuration:
- **Organization:** `Cognitive-QE-Labs`
- **Organization URL:** `https://dev.azure.com/Cognitive-QE-Labs`
- **Project Name:** `MultiAgent-Test-Framework`

---

## 🔧 Step 1: Get Your Google Gemini API Key

1. Visit: https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click "+ Create API Key"
4. Select "Create API key in new project"
5. Copy the generated API key
6. **For production use, enable billing:**
   - Go to: https://console.cloud.google.com
   - Select your project
   - Go to Billing
   - Link a billing account
   - This removes the 429 quota limits

---

## 🔧 Step 2: Create Azure DevOps Personal Access Token

**Do this AFTER revoking the exposed token:**

1. Go to: https://dev.azure.com/Cognitive-QE-Labs/_usersSettings/tokens
2. Click "+ New Token"
3. Fill in the details:
   - **Name:** `AQEE-Production`
   - **Organization:** `Cognitive-QE-Labs`
   - **Expiration:** `90 days`
4. Select scopes (check exactly these):
   - ✅ Work Items → Read & Write
   - ✅ Test Management → Read & Write
   - ☐ All other scopes can be unchecked
5. Click "Create"
6. **COPY THE TOKEN IMMEDIATELY** - it won't be shown again
7. Store it safely (we'll use it next)

---

## 📁 Step 3: Create Your .env File

The `.env` file stores your credentials **locally only** - it is NOT committed to Git.

### Option A: Using PowerShell

```powershell
# Navigate to your project directory
cd c:\src\qa-agent-ecosystem

# Copy the example file
Copy-Item .env.example .env

# Edit with Notepad
notepad .env
```

Then add your credentials:
```dotenv
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE
AZURE_DEVOPS_TOKEN=YOUR_NEW_AZURE_PAT_HERE
AZURE_DEVOPS_ORG_URL=https://dev.azure.com/Cognitive-QE-Labs
AZURE_DEVOPS_PROJECT=MultiAgent-Test-Framework
```

### Option B: Using Python

```powershell
# Navigate to your project directory
cd c:\src\qa-agent-ecosystem

# Run this command in PowerShell
python -c "
with open('.env.example', 'r') as src:
    content = src.read()
with open('.env', 'w') as dst:
    dst.write(content)
print('✓ .env file created from .env.example')
print('✓ Now edit .env with your actual credentials')
"

# Then edit .env with your credentials
notepad .env
```

---

## 🔐 Your Credentials to Use

Fill in your `.env` file with these values:

```dotenv
# Google API Key
GOOGLE_API_KEY=YOUR_GOOGLE_GEMINI_API_KEY

# Azure DevOps
AZURE_DEVOPS_TOKEN=YOUR_NEW_PERSONAL_ACCESS_TOKEN
AZURE_DEVOPS_ORG_URL=https://dev.azure.com/Cognitive-QE-Labs
AZURE_DEVOPS_PROJECT=MultiAgent-Test-Framework
```

---

## ✅ Step 4: Verify Your Configuration

### Check Credentials Are Loaded

```powershell
# Navigate to project
cd c:\src\qa-agent-ecosystem

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Run verification script
python test_agents.py
```

Expected output:
```
✓ Root agent loaded: AQEE_Orchestrator
✓ Model: gemini-3-flash
✓ Sub-agents count: 7
✓ Sub-agents:
  - Requirement_Architect
  - Project_Planner
  - TestCase_Designer
  - Test_Executor
  - Report_Generator
  - Issue_Tracker
  - Resource_Planner
✓ Tools count: 1

✅ All agents loaded successfully!
```

If you see warnings like "Missing credentials: ...", double-check your `.env` file is correctly formatted.

---

## 🚀 Step 5: Launch AQEE

```powershell
# Navigate to project
cd c:\src\qa-agent-ecosystem

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Set Python path
$env:PYTHONPATH = 'C:\src\qa-agent-ecosystem'

# Launch AQEE web interface
adk web --port 8000
```

You should see:
```
Starting ADK web server on http://localhost:8000
Press Ctrl+C to stop the server
```

### Open in Browser

1. Open your browser
2. Go to: http://localhost:8000
3. Click the dropdown and select **AQEE_Orchestrator**
4. Start asking questions!

Example prompts:
- "Create a comprehensive test plan for a payment module"
- "Design test cases for user login functionality"
- "Analyze requirements and create Azure DevOps work items"

---

## 🔄 Credential Rotation (Do This Every 90 Days)

Every 90 days, generate a new Azure DevOps token:

1. Go to: https://dev.azure.com/Cognitive-QE-Labs/_usersSettings/tokens
2. Find your old `AQEE-Production` token
3. Click "..." → "Revoke"
4. Click "+ New Token" and repeat Step 2 above
5. Update your `.env` file with the new token

---

## 🆘 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'agent'"
**Solution:** Set PYTHONPATH before running adk:
```powershell
$env:PYTHONPATH = 'C:\src\qa-agent-ecosystem'
adk web
```

### Issue: "429 RESOURCE_EXHAUSTED"
**Solution:** Enable billing on your Google Cloud project:
1. Go to: https://console.cloud.google.com
2. Select your project
3. Go to Billing → Link billing account
4. Wait a few minutes, then retry

### Issue: "401 Unauthorized" with Azure
**Solution:** Check your token and org URL:
```powershell
# Verify the token is set
$env:AZURE_DEVOPS_TOKEN

# Verify the org URL is correct (should be):
# https://dev.azure.com/Cognitive-QE-Labs
$env:AZURE_DEVOPS_ORG_URL
```

### Issue: ".env file not being read"
**Solution:** Verify .env is in the correct location:
- Must be in: `c:\src\qa-agent-ecosystem\.env`
- Verify it's not named `.env.txt` or similar
- Check file exists: `Test-Path .\.env`

---

## 📚 Next Steps

1. Review [README.md](README.md) for feature overview
2. Read [SECURITY.md](SECURITY.md) for security best practices
3. Try example prompts in the AQEE UI
4. Review agent capabilities in [README.md](README.md#agent-capabilities)

---

## 🎯 Quick Reference

**File Locations:**
- `.env` → Local credentials (ignored by git)
- `.env.example` → Template for .env
- `agent.py` → Root orchestrator (AQEE_Orchestrator)
- `agents/` → 7 specialized agents

**Key Commands:**
```powershell
# Activate environment
.venv\Scripts\Activate.ps1

# Verify installation
python test_agents.py

# Launch AQEE
$env:PYTHONPATH = 'C:\src\qa-agent-ecosystem'; adk web

# Run any Python file
python -m agents.architect
```

**Important URLs:**
- Google Gemini API: https://aistudio.google.com/app/apikey
- Azure PAT Generator: https://dev.azure.com/Cognitive-QE-Labs/_usersSettings/tokens
- AQEE Web UI: http://localhost:8000

---

**Setup complete!** 🎉

For more help, see [SECURITY.md](SECURITY.md) and [README.md](README.md)
