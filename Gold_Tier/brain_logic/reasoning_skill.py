from brain_logic.base_skill import BaseSkill

class ReasoningSkill(BaseSkill):
    def __init__(self):
        super().__init__("Reasoning", "General AI Employee Reasoning Engine")

    def run_task(self, context_content: str, task_type: str, handbook: str):
        prompt = f"""
[AGENTIC TASK TRIGGER]
You are an AI Employee. I have a new task for you.

--- HANDBOOK ---
{handbook}

--- TASK CONTEXT ---
{context_content}

--- INSTRUCTION ---
1. You are in the 'Reasoning' phase. Your goal is to produce the final content for approval.
2. If this is a SOCIAL task, use the 'social-media-manager' skill logic to write the post content. 
   - MANDATORY: Include a note at the end of every post: "This post was created by a Personal AI Employee."
3. If this is an EMAIL task, use the 'email-agent' skill logic to draft the reply.
   - MANDATORY: Always sign off as "Aashra's AI Employee" (DO NOT use "Your AI Employee").
4. If this is an ACCOUNTING task, use the 'odoo-accounting' skill logic to prepare the data.
5. IMPORTANT: DO NOT attempt to write any files to the filesystem yourself.
6. IMPORTANT: DO NOT return a 'type: reasoning' request. Return the FINAL action request (e.g., type: linkedin_post, type: email_response).

7. Respond ONLY with the text content for the following sections:
   
   PLAN:
   [Your multi-step execution plan]

   ## ACTION_REQUEST
   ---
   type: [e.g., linkedin_post, twitter_post, email, odoo_invoice]
   
   [METADATA SECTION - if applicable]
   To: [Recipient Email]
   Subject: [Email Subject]
   Client: [Client Name for Odoo]
   Amount: [Amount for Odoo]
   Desc: [Description for Odoo]

   ## Content
   [THE ACTUAL FINAL CONTENT TO BE POSTED OR SENT]
   ---

Ensure the ACTION_REQUEST block contains the ACTUAL CONTENT you want the human to approve.
Use '## Content' as the header for the main body of the post or email.
DO NOT use YAML block syntax (like 'content: |') inside the ACTION_REQUEST. Use plain text headers.
"""
        return self.execute(prompt)
