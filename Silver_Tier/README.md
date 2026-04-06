# 🤖 Personal AI Employee (Digital FTE) - Silver Tier

Welcome to the future of work. This project is a **Digital FTE (Full-Time Equivalent)** designed to operate autonomously in 2026. 

### **What does this project actually do?**
This is a local-first automation system that **manages your professional life** by:
1.  **Handling your Gmail:** It monitors your inbox, understands incoming emails, and drafts professional replies automatically.
2.  **Growing your LinkedIn:** It takes your raw ideas and automatically turns them into high-quality LinkedIn posts to drive business growth.

It acts as your proactive business partner, working 24/7 using Claude Code as its reasoning engine and Obsidian as its management dashboard. You simply review and approve the AI's work before it goes live.

---

## 🌟 Project Vision
A Digital FTE isn't just a chatbot; it’s a proactive business partner. While a human works 2,000 hours a year, this agent works **8,760 hours**, reducing task costs by up to 90%. It lives in your local environment, keeping your data private while automating your "Senses" (Watchers) and "Hands" (MCP Servers).

---

## 🚀 What This Silver Tier Does
The Silver Tier elevates the automation by introducing **Human-in-the-Loop execution**. It doesn't just process data; it prepares actions and waits for your signal.

✔ **Monitors Gmail:** Automatically pulls unread emails into your Obsidian Inbox.
✔ **LinkedIn Content:** Watches for post ideas and drafts professional social media content.
✔ **AI Reasoning:** Uses Claude to generate detailed **PLANs** and **PENDING** action drafts based on your `Company_Handbook.md`.
✔ **Approval System:** Provides a safety gate where tasks are only executed once you move them to the `Approved` folder.
✔ **Automated Execution:** Once approved, the system "Hands" (MCP Servers) automatically send emails or post to LinkedIn.

---

## 🏗️ Architecture & Tech Stack

### 1. The Brain (Reasoning)
- **Claude Code (CCR):** Acts as the central reasoning engine. It analyzes incoming data, consults the `Company_Handbook.md`, and formulates plans.
- **Reasoning Loop:** Every input goes through a "Research -> Strategy -> Execution" cycle.

### 2. The Memory & GUI (Dashboard)
- **Obsidian Vault:** Your local Markdown-based command center. 
  - `/Needs_Action`: Incoming tasks from watchers.
  - `/Plans`: AI-generated strategies for each task.
  - `/Approval`: Human-in-the-loop folder (`Pending` -> `Approved`).
  - `/Executed`: History of completed tasks.

### 3. The Senses (Watchers)
Lightweight Python scripts that monitor the world:
- **Gmail Watcher:** Monitors unread emails and pulls them into the vault.
- **LinkedIn Watcher:** Watches for post ideas/content in the `Events` folder.
- **Execution Watcher:** The bridge between the vault and the AI brain.

### 4. The Hands (MCP - Model Context Protocol)
Dedicated servers to interact with the external world:
- **Email Server:** Uses Gmail API to send approved replies.
- **LinkedIn Server:** Simulates/Posts content to social media to drive business growth.

---

## 🚀 Key Features (Silver Tier)
- **Proactive Automation:** The system wakes up and works without waiting for user prompts.
- **Human-in-the-Loop:** Sensitive actions (like sending an email or posting) require you to move a file to the `Approved` folder.
- **Handbook-Driven:** The AI reads your `Company_Handbook.md` to learn your tone, rules, and business logic.
- **Autonomous Posting:** Automatically generates social media content from simple ideas to help you generate sales.

---

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.13+
- Node.js v24+
- Claude Code CLI (`ccr.cmd`)
- Google Cloud Console Project (with Gmail API enabled and `credentials.json`)

### Installation
1. **Clone the project** and navigate to the directory.
2. **Install Dependencies:**
   ```bash
   pip install google-api-python-client google-auth-oauthlib google-auth-httplib2 requests
   ```
3. **Configure Gmail:**
   Place your `credentials.json` in the root folder.
4. **Initialize Obsidian:**
   Open the `AI_Employee_Vault` folder as a new vault in Obsidian.

---

## 🔄 How to Use

### 1. Start the System
Run the system in a continuous loop:
```bash
python run_system.py --loop
```

### 2. The Workflow
1. **Inbox:** An email arrives or you drop a LinkedIn idea into `Events/LinkedIn_Ideas`.
2. **AI Reasoning:** The system detects it, creates a `PLAN` and a `PENDING` request in your Obsidian vault.
3. **Review:** You open Obsidian, read the AI's draft in `Approval/Pending`.
4. **Approve:** Move the `.md` file to `Approval/Approved`.
5. **Execute:** On the next cycle, the AI sends the email or logs the social post, moving the record to `Executed`.

---

## 🔑 Credential & Token Guide

This project requires several API keys and credentials. Here is how to get them:

### 1. Gmail (App Passwords)
- **Why?** To read and send emails securely.
- **How?** 
    - Go to your Google Account -> Security.
    - Enable **2-Factor Authentication**.
    - Search for **"App Passwords"**.
    - Generate a new password for "Mail" and "Windows Computer".
    - Save this in `.env` as `APP_PASSWORD`.

### 2. LinkedIn API
- **The Challenge**: LinkedIn's API requires specific permissions (`w_member_social`) to post on a personal profile.
- **How to Get Secrets**:
    1. Create an app on the [LinkedIn Developers Portal](https://www.linkedin.com/developers/).
    2. Under **Products**, add "Share on LinkedIn" and "Sign In with LinkedIn".
    3. In the **Auth** tab, find your **Client ID** and **Client Secret**.
    4. **Generate Access Token**:
       - Use the [LinkedIn OAuth 2.0 Tools](https://www.linkedin.com/developers/tools/oauth) or a script to get a **3-legged Access Token**.
       - Ensure you select the `w_member_social` and `openid profile` scopes.
    5. **Find your Person ID (URN)**:
       - Once you have the token, call the `me` endpoint:
         ```bash
         curl -X GET "https://api.linkedin.com/v2/me" -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
         ```
       - The `id` field in the response (e.g., `urn:li:person:ABC123XYZ`) is your **LINKEDIN_PERSON_ID**.
    6. Save `LINKEDIN_ACCESS_TOKEN` and `LINKEDIN_PERSON_ID` in your `.env`.

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
Silver_Tier/
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

## 📈 Use Cases
- **Customer Support:** Automatically drafting replies to common inquiries.
- **Lead Generation:** Posting daily business insights to LinkedIn from raw notes.
- **Business Audit:** The AI can summarize your dashboard to give you a "Monday Morning CEO Briefing."

---

## 📜 Project Structure
```text
Silver_Tier/
├── AI_Employee_Vault/       # Your Obsidian Management Vault
├── mcp_server/              # External Action Servers (Email, LinkedIn)
├── watchers/                # Monitoring Scripts (Gmail, Execution)
├── run_system.py            # Main Orchestrator
├── credentials.json         # Your Google API Key (Private)
└── README.md                # This Guide
```

---

## 🤝 Conclusion
This Personal AI Employee is designed to take your "Business on Autopilot." By combining local privacy with the reasoning power of Claude, it creates a scalable unit of value that grows with your needs.

**Built for the 2026 AI Employee Hackathon.**
