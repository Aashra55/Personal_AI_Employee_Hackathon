from brain_logic.base_skill import BaseSkill

class ReasoningSkill(BaseSkill):
    def __init__(self):
        super().__init__("Reasoning", "General AI Employee Reasoning Engine")

    def run_task(self, context_content: str, task_type: str, handbook: str):
        # We no longer provide instructions here. 
        # We tell Claude to discover and use the Agent Skills in .claude/skills/
        
        prompt = f"""
[AGENTIC TASK TRIGGER]
You are an AI Employee. I have a new task for you.

--- HANDBOOK ---
{handbook}

--- TASK CONTEXT ---
{context_content}

--- INSTRUCTION ---
1. Identify the correct Agent Skill from your '.claude/skills/' directory (e.g., reasoning-engine, odoo-accounting, social-media-manager).
2. Execute that skill to process the context above.
3. Respond with the generated PLAN and ACTION_REQUEST as defined in your skill instructions.
"""
        return self.execute(prompt)
