---
name: ceo-audit-briefing
description: Use this skill to perform weekly business and accounting audits and generate executive briefings for the CEO.
---

# CEO Audit & Briefing Skill (The Analyst)

## Instructions
1. **Execution:** To generate a briefing, run the internal script `generate_audit.py`:
   `python generate_audit.py`
2. **Data Collection:** Scan `mcp_server/odoo_audit.log` and `mcp_server/social_audit.log`.
3. **Analysis:** Identify key financial metrics, social engagement levels, and system errors.
4. **Report Generation:** Create `AI_Employee_Vault/Archive/Reports/CEO_BRIEFING_[DATE].md`.

   - Include sections: Financial Health, Social Impact, System Status, and Strategic Recommendations.
4. **Traceability:** Link all summaries back to their respective `PLAN.md` files in the Vault.

## Examples
- **Trigger:** End of business week or manual audit request.
- **Action:** Compile all logs into a structured 1-page markdown briefing for the CEO.
