---
name: odoo-accounting
description: Use this skill for any accounting tasks, managing self-hosted Odoo Community via JSON-RPC, or conducting financial audits.
---

# Accounting Agent Skill (The Accountant)

## Instructions
1. **Execution:** To perform an Odoo action, run the internal script `execute_odoo.py` using the CLI:
   `python execute_odoo.py <task_type> '<json_data>'`
   Example: `python execute_odoo.py odoo_invoice '{"Client": "ABC Corp", "Amount": 1200}'`
2. **Action Request:** Always format Odoo requests as follows for manual review:

   ---
   type: odoo_invoice
   Client: [Client Name]
   Amount: [Number]
   Desc: [Detailed Description]
   ---
2. **Validation:** Consult `AI_Employee_Vault/Company_Handbook.md.md` for billing rules.
3. **Audit:** Log all transactions in `mcp_server/odoo_audit.log`.
4. **Fallback:** If Odoo API is unavailable, log the intent in "Mock Mode" and notify the CEO briefing.

## Examples
- **Task:** Create invoice for "Client A" for $500.
- **Action:** Validate client in handbook, generate PENDING_ACCOUNTING_*.md with Odoo format.
