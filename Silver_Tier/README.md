# 🤖 Personal AI Employee (Digital FTE) - Silver Tier

Welcome to the future of work. This project is a **Digital FTE (Full-Time Equivalent)** designed to operate autonomously in 2026. It is a local-first, agent-driven system that manages your personal and business affairs 24/7 using Claude Code as its reasoning engine and Obsidian as its management dashboard.

---

## 🌟 Project Vision
A Digital FTE isn't just a chatbot; it’s a proactive business partner. While a human works 2,000 hours a year, this agent works **8,760 hours**, reducing task costs by up to 90%. It lives in your local environment, keeping your data private while automating your "Senses" (Watchers) and "Hands" (MCP Servers).

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
**CEO:** Aashra Saleem
