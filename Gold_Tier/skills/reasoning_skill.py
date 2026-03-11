from skills.base_skill import BaseSkill

class ReasoningSkill(BaseSkill):
    def __init__(self):
        super().__init__("Reasoning", "General AI Employee Reasoning Engine")

    def run_task(self, context_content: str, task_type: str, handbook: str):
        if task_type == "social":
            instruction = """
1. Analyze the social media idea.
2. Create a 'PLAN' in markdown.
3. Create an 'ACTION_REQUEST' with EXACT format:
   ---
   type: [facebook_post | instagram_post | twitter_post]
   ## Content / Body
   [Post content]
   ---
"""
        elif task_type == "accounting":
             instruction = """
1. Analyze the invoice/financial request.
2. Create a 'PLAN' in markdown.
3. Create an 'ACTION_REQUEST' with EXACT format:
   ---
   type: odoo_invoice
   Client: [Client Name]
   Amount: [Number]
   Desc: [Description]
   ---
"""
        else: # Email fallback
            instruction = """
1. Analyze the email based on Handbook.
2. Create a 'PLAN' in markdown.
3. Create an 'ACTION_REQUEST' with EXACT format:
   ---
   type: email
   To: [Sender Email]
   Subject: Re: [Original Subject]
   ## Content / Body
   [Your reply]
   ---
"""

        prompt = f"""
You are an AI Employee Reasoning Engine. 
Use the following Company Handbook and Context.

--- HANDBOOK ---
{handbook}

--- CONTEXT ---
{context_content}

--- TASK ---
{instruction}

Respond STRICTLY with the PLAN and ACTION_REQUEST.
"""
        return self.execute(prompt)
