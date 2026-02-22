# 🧠 Personal AI Employee – Bronze Tier

An automated AI-powered workflow that monitors Gmail, converts emails into structured Markdown inside an Obsidian Vault, processes them using Claude Code Router (CCR), and moves completed tasks to a Done folder.

This project demonstrates the foundation of an autonomous AI Employee.

---

# 🚀 What This Bronze Tier Does

✔ Monitors Gmail for unread emails
✔ Saves them as structured Markdown files
✔ Sends content to Claude Code Router 
✔ Appends AI decision + draft reply
✔ Moves processed email to `/Done`

This creates an automated AI workflow inside an Obsidian vault.

---

# 📁 Project Structure

```
Personal_AI_Employee_Hackathon/
│
├── Bronze_Tier/
│   ├── base_watcher.py
│   ├── gmail_watcher.py
│   ├── run_watcher.py
│   ├── credentials.json (NOT committed)
│   ├── token.json (NOT committed)
│   ├── .gitignore
│   │
│   └── AI_Employee_Vault/
│       ├── Company_Handbook.md
│       ├── Dashboard.md
│       ├── Inbox/
│       ├── Needs_Action/
│       └── Done/
```

---

# ⚙️ Requirements

* Python 3.10+
* Node.js (for CCR)
* Gmail account
* Google Cloud Console access
* Obsidian (optional but recommended)

---

# 🔐 Google Gmail API Setup (credentials.json process)

## Step 1: Create Google Cloud Project

1. Go to Google Cloud Console
2. Click **Create Project**
3. Name it (example: Personal AI Employee)
4. Select project after creation

---

## Step 2: Enable Gmail API

1. Go to **APIs & Services → Library**
2. Search: Gmail API
3. Click **Enable**

---

## Step 3: Create OAuth Credentials

1. Go to **APIs & Services → Credentials**
2. Click **Create Credentials**
3. Select **OAuth Client ID**
4. If prompted, configure Consent Screen:

   * User Type: External
   * App name: Personal AI Employee
   * Add your email
5. Create OAuth Client ID:

   * Application Type: Desktop App
6. Download JSON file

Rename downloaded file to:

```
credentials.json
```

Place it inside:

```
Bronze_Tier/
```

⚠️ Do NOT upload this file to GitHub.

---

# 🔄 How token.json Is Generated

`token.json` is automatically generated the first time you run:

```
python run_watcher.py
```

Process:

* Browser opens
* You log in to Gmail
* You grant access
* OAuth access + refresh token is saved locally as `token.json`

This token allows automation to access Gmail without logging in repeatedly.

⚠️ Never push this file to GitHub.

---

# 🔐 .gitignore Setup

Inside `Bronze_Tier/.gitignore`:

```
.env
credentials.json
token.json
```

---

# 🛅 Environment Variables

GMAIL_ACCOUNT=youremail@gmail.com
APP_PASSWORD=abcd efgh ijkl mnop 

---

# 🤖 Claude Code Router (CCR) Setup

## Step 1: Install CCR

```
npm install -g @musistudio/claude-code-router
```

Verify installation:

```
ccr --version
```

---

## Step 2: How CCR Is Triggered

Inside `gmail_watcher.py`:

```python
subprocess.run(
    ["ccr.cmd", "code"],
    shell=True,
    input=prompt,
    capture_output=True,
    text=True,
    check=True
)
```

This sends structured email data to CCR and returns AI-generated Markdown.

---

# 🧠 AI Workflow Logic

1. GmailWatcher checks unread emails
2. Creates Markdown file in `/Needs_Action`
3. Sends email data to CCR
4. CCR generates:

   * Decision
   * Action
   * Draft Reply
5. AI result appended to file
6. File moved to `/Done`

---

# 🏢 Company_Handbook.md Purpose

Defines:

* Email handling rules
* Folder structure
* Decision priority
* Agent behavior instructions

Acts as control policy for the AI employee.

---

# ▶ How to Run

From project root:

```
cd Bronze_Tier
python run_watcher.py
```

Expected output:

```
[+] Email saved
[✓] CCR processed successfully
[✓] Email processed and moved to Done
```

---

# ⚠️ Common Errors & Fixes

### WinError 2

Cause: CCR not in PATH
Fix: Use `ccr.cmd` with `shell=True`

---

# 🛡 Security Notes

* Never commit credentials.json
* Never commit token.json
* Rotate credentials if exposed
* Use environment variables in production systems

---

# 🎯 Bronze Tier Completion Summary

✔ Gmail Automation
✔ Obsidian Vault Integration
✔ AI Decision Engine via CCR
✔ Secure OAuth Implementation
✔ Folder-based AI Workflow

This project establishes a working Personal AI Employee foundation.
