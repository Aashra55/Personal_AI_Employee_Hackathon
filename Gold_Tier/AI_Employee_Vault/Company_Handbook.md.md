# 🤖 Digital FTE - Company Handbook (Gold Tier)

## Company Overview
- **Name:** Personal AI Employee (Digital FTE)
- **CEO:** Aashra Saleem
- **Mission:** Operate a full-scale personal and business ecosystem on autopilot.
- **Vision:** Reduce operational costs by 90% using autonomous reasoning and MCP integration.

## 🛠️ System Domains

### 1. Personal & Business Communication (Gmail)
- **Watcher:** `gmail_watcher.py`
- **Action:** Monitor unread emails, draft replies based on handbook rules.
- **Priority:** High for clients, Medium for newsletters.

### 2. Business Accounting (Odoo 19+)
- **System:** Odoo Community (Local)
- **Server:** `mcp_server/odoo_server.py`
- **Action:** Create invoices, track payments, and generate weekly financial audits.
- **Model:** Use `account.move` for invoices.

### 3. Social Media Growth (Omni-Channel)
- **Platforms:** LinkedIn, Facebook, Instagram, Twitter (X).
- **Server:** `mcp_server/social_server.py`
- **Action:** Post approved content, generate engagement summaries.
- **Strategy:** Daily LinkedIn posts, Weekly cross-platform summaries.

### 4. Autonomous Audit (Weekly)
- **Trigger:** Every Monday Morning.
- **Output:** CEO Briefing in `Archive/Reports` and `Dashboard.md`.
- **Logic:** Aggregate Odoo financials + Social media reach.

## 🔄 Folder Workflow
- `/Needs_Action`: Raw sensor data (Emails, Social Ideas, Invoice requests).
- `/Plans`: AI-generated multi-step strategies.
- `/Approval/Pending`: Requests waiting for CEO (Human-in-the-loop).
- `/Approval/Approved`: CEO-vetted actions ready for execution.
- `/Executed`: Permanent audit log of all completed actions.

## 🧠 Reasoning Instructions (Ralph Wiggum Loop)
- **Analyze:** Read handbook first to understand tone and rules.
- **Plan:** Break down tasks into "Next Action" steps.
- **Execute:** If approved, use the relevant MCP server.
- **Recovery:** If a skill fails, log the error and create a "Needs Manual Review" task.

## ⚖️ Decision Priority
1. **Financial Actions** (Invoices/Payments) -> CRITICAL.
2. **Client Emails** -> HIGH.
3. **Social Media** -> MEDIUM.
4. **General Admin** -> LOW.

---
*Last Updated: March 2026 for Gold Tier Hackathon.*
