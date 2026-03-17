---
name: social-media-manager
description: Use this skill to manage social media postings across Facebook, Instagram, LinkedIn, and X (Twitter), ensuring brand voice consistency.
---

# Social Media Manager Skill (The Marketer)

## Instructions
1. **Execution:** To post content, run the internal script `post_social.py` for each platform (facebook, instagram, twitter, linkedin):
   `python post_social.py <platform> '<content_body>'`
2. **Omni-Channel Strategy:** For every approved idea, generate content for all connected platforms (FB, IG, X, LinkedIn).
3. **Format:** Use platform-specific ACTION_REQUESTs:

   ---
   type: [facebook_post | instagram_post | twitter_post | linkedin_post]
   ## Content / Body
   [Post content with relevant hashtags]
   ---
3. **Summarization:** After processing a batch of posts, create a summary in `AI_Employee_Vault/Executed/`.
4. **Tone:** Adhere strictly to the brand voice in `Company_Handbook.md`.

## Examples
- **Task:** Post about "AI Benefits" to all platforms.
- **Action:** Generate three unique PENDING files for FB, IG, and X.
