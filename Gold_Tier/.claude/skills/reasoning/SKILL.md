---
name: reasoning-engine
description: Use this skill when you need to analyze incoming data, consult the Company Handbook, and generate a multi-step execution plan for an AI employee task.
---

# Reasoning Agent Skill (The Brain)

## Instructions
1. **Analyze:** When a new file appears in `AI_Employee_Vault/Needs_Action/`, read its content and the `AI_Employee_Vault/Company_Handbook.md.md`.
2. **Plan:** Create a `PLAN.md` in `AI_Employee_Vault/Plans/`. 
   - Outline the objective.
   - List steps for execution.
   - Specify the target MCP server (Odoo, Social, or Email).
3. **Draft Action:** Generate a `PENDING_*.md` file in `AI_Employee_Vault/Approval/Pending/`.
   - Use the exact format required for the target MCP server.
4. **Log:** Move the original request to `AI_Employee_Vault/Reasoned/` to prevent duplicate processing.

## Examples
- **Input:** `SOCIAL_post_idea.md` in Needs_Action.
- **Action:** Read handbook, draft plan for FB/IG/X, create PENDING_SOCIAL_*.md.
