# 🏗️ Personal AI Employee Architecture (Gold Tier)

## 1. Overview
The **Digital FTE** is an autonomous multi-agent system designed to handle the complexity of both personal and business operations. It follows a "Senses -> Brain -> Hands" (Watchers -> Reasoning -> MCP) architecture, ensuring local-first privacy with high-scale AI capabilities.

---

## 2. Core Components

### 👁️ Senses (Watchers)
- **GmailWatcher:** Monitors unread emails.
- **LinkedInWatcher:** Monitors content ideas.
- **ExecutionWatcher:** Monitors the reasoning queue.
- **ApprovalWatcher:** Monitors human-vetted actions.
- **AuditWatcher:** Monitors the temporal schedule (Weekly Briefing).

### 🧠 Brain (Reasoning Skill)
- **ReasoningSkill:** Encapsulates the AI's logic. It uses the **Company Handbook** as a system prompt to maintain brand consistency and operational logic.
- **Multi-Step Planning:** Generates a structured `PLAN.md` before any action is requested.

### 🧤 Hands (MCP Servers)
- **Odoo Server:** Handles accounting via JSON-RPC.
- **Social Server:** Manages Omni-channel posting (FB, IG, X).
- **Email Server:** Interfaces with Gmail API.

---

## 3. Data Flow (Ralph Wiggum Loop)
1. **Detection:** A watcher finds new data and places it in `/Needs_Action`.
2. **Reasoning:** `ExecutionWatcher` activates the `ReasoningSkill` to create a `PLAN` and a `PENDING` request.
3. **Approval:** A human (CEO) reviews and moves the request to `/Approved`.
4. **Execution:** `ApprovalWatcher` detects the move and calls the relevant MCP server.
5. **Finalization:** The record is moved to `/Executed` for audit logging.
6. **Recurrence:** The loop resets immediately if work was processed (Work-done > 0), or sleeps for 60s.

---

## 4. Error Recovery & Graceful Degradation
- **Connectivity:** Each MCP server (Odoo, Social) implements a "Mock Mode" fallback. If real credentials aren't found, it logs a simulation to ensure the system doesn't crash.
- **AI Failure:** If the Reasoning Skill fails to parse, a "Manual Review Required" task is generated.

---

## 5. Lessons Learned
- **Prompt Engineering is Branding:** The AI's personality is entirely defined by the `Company_Handbook.md`. Keeping this updated is critical for high-quality output.
- **Local First, Global Action:** Keeping the state in Markdown (Obsidian) makes the system transparent, debuggable, and incredibly reliable compared to a black-box database.
- **Humans are the Bottleneck:** The "Human-in-the-loop" approval process is the most important security feature, preventing the AI from spending money or posting sensitive content without oversight.

---
*Created for the 2026 AI Employee Hackathon.*
