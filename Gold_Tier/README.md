# 🤖 Gold Tier: Personal AI Employee Hackathon

Welcome to the **Gold Tier AI Employee** project. This is a sophisticated automation system designed to act as a digital member of your team. It doesn't just run scripts; it **monitors, reasons, asks for approval, and executes** tasks across Gmail, Accounting (Odoo), and Social Media (X, LinkedIn, Instagram, Facebook).

---

## 🌟 Project Vision
The goal of this project is to create a "Human-in-the-Loop" AI agent. It handles the complete lifecycle of tasks—from **monitoring and drafting** to **final execution and posting** (on X, LinkedIn, Instagram and Facebook)—while keeping a human supervisor in control via an easy approval system.

---

## 🛠️ Tech Stack & Architecture

### Core Technologies
- **Claude**: The "Brain" of the system. We use Claude Router for high-level reasoning, intent extraction from emails, and creative drafting.
- **Python 3.10+**: The primary engine.
- **Selenium (Chrome)**: Used for browser automation to bypass API restrictions (especially for X/Twitter).
- **MCP (Model Context Protocol)**: Specialized servers located in `mcp_server/` to handle specific platform logic.

### System Components
1. **Watchers (`watchers/`)**: Continuous background scripts that monitor Gmail, Odoo, and Social Media folders.
2. **AI Vault (`AI_Employee_Vault/`)**: A markdown-based database that stores every plan, approval request, and executed action.
3. **Reasoning Skill (`skills/`)**: This is where Claude processes the input. It reads the `Company_Handbook.md` and the detected task, then decides the best strategy, creating a structured `PLAN.md`.
4. **MCP Servers (`mcp_server/`)**: The "Hands" that physically execute Claude's decisions—sending emails, posting to social media, or creating Odoo invoices.

---

## 🔄 The Workflow (Life of a Task)
1. **Detect**: A Watcher finds a new email or social media idea.
2. **Reason**: The system creates a `PLAN` and a `PENDING` approval request in the Vault.
3. **Approve**: A human moves the file from `Approval/Pending` to `Approval/Approved`.
4. **Execute**: The `approval_watcher` detects the move and triggers the relevant MCP server to perform the task.
5. **Archive**: The task is moved to `Executed` with a success timestamp.

---

## 🔑 Credential & Token Guide

This project requires several API keys and credentials. Here is how to get them:

### 1. Gmail (App Passwords)
- **Why?** To read and send emails securely.
- **How?** 
    - Go to your Google Account -> Security.
    - Enable **2-Factor Authentication**.
    - Search for **"App Passwords"**.
    - Generate a new password for "Mail" and "Windows Computer".
    - Save this in `.env` as `APP_PASSWORD`.

### 2. X (Twitter) Developer & Selenium
- **The Challenge**: Twitter API (v2) often requires a paid tier ($100/mo) to post.
- **The Solution**: We use a **Selenium Fallback** with a Persistent Profile.
- **Setup**:
    - For API usage (monitoring): Go to [developer.twitter.com](https://developer.twitter.com), create a project, and get your Keys/Tokens.
    - **Crucial**: Ensure App Permissions are set to "Read and Write".
    - **Selenium Profile**: The first time you run a tweet, a browser window will open. Log in **manually**. The system will save your session in `mcp_server/twitter_profile/` so you never have to log in again.

### 3. Facebook & Instagram (Meta for Developers)
- **The Challenge**: Posting to Facebook requires a **Page Access Token**, not just a standard User token.
- **The Process**:
    1. Go to [developers.facebook.com](https://developers.facebook.com) and create a Business App.
    2. Add **Graph API** to your app and use the **Graph API Explorer**.
    3. Generate a **User Access Token** with `pages_manage_posts`, `pages_read_engagement`, and `pages_show_list` permissions.
    4. Copy this token into your `.env` as `FB_ACCESS_TOKEN`.
    5. **Run the Diagnostic Tool**:
       ```bash
       python mcp_server/diag_fb.py
       ```
    6. This script will inspect your token and list all **Facebook Pages** you manage.
    7. **Crucial**: From the output of `diag_fb.py`, copy the specific **Page ID** and the **Page Access Token** provided for your desired page into your `.env`. 
    8. **Verify**: Run `diag_fb.py` again with the new Page Token to ensure the type has changed from `USER` to `PAGE`.
    9. Use the **Access Token Debugger** on Meta's site to "Extend" this token to make it **Permanent** (Never Expire).

### 4. LinkedIn API
- **The Challenge**: LinkedIn's API requires specific permissions (`w_member_social`) to post on a personal profile.
- **How to Get Secrets**:
    1. Create an app on the [LinkedIn Developers Portal](https://www.linkedin.com/developers/).
    2. Under **Products**, add "Share on LinkedIn" and "Sign In with LinkedIn".
    3. In the **Auth** tab, find your **Client ID** and **Client Secret**.
    4. **Generate Access Token**:
       - Use the [LinkedIn OAuth 2.0 Tools](https://www.linkedin.com/developers/tools/oauth) or a script to get a **3-legged Access Token**.
       - Ensure you select the `w_member_social` and `openid profile` scopes.
    5. **Find your Person ID (URN)**:
       - Once you have the token, call the `me` endpoint:
         ```bash
         curl -X GET "https://api.linkedin.com/v2/me" -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
         ```
       - The `id` field in the response (e.g., `urn:li:person:ABC123XYZ`) is your **LINKEDIN_PERSON_ID**.
    6. Save `LINKEDIN_ACCESS_TOKEN` and `LINKEDIN_PERSON_ID` in your `.env`.

### 5. Instagram (Graph API)
- **Prerequisite**: You must have an **Instagram Business Account** linked to a **Facebook Page**.
- **How to get INSTA_USER_ID**:
    1. First, complete the **Facebook & Instagram (Meta for Developers)** section above to get your `FB_ACCESS_TOKEN` and `FB_PAGE_ID`.
    2. Ensure `INSTA_USERNAME` and `INSTA_PASSWORD` are saved in your `.env` file.
    3. Run the Instagram Diagnostic Tool:
       ```bash
       python mcp_server/diag_insta.py
       ```
    4. This script will query the Graph API and provide the **Instagram Business Account ID** linked to your Page.
    5. Copy the provided ID into your `.env` as `INSTA_USER_ID`.
    6. **Default Image Fallback**:
       - **For Graph API**: Save a public image URL as `INSTA_DEFAULT_IMAGE_URL` in your `.env`. This is used if no image is provided in the task or if the provided URL is broken.
       - **For Selenium**: Ensure `mcp_server/ig_placeholder.png` exists. This local file acts as the default fallback for browser-based automation when no other image is specified.
    7. These configurations ensure your Instagram posts never fail due to missing media.

### 6. Odoo (Accounting)
- **How?**
    - Use your Odoo instance URL (e.g., `https://yourcompany.odoo.com` or `http://localhost:8069`).
    - **Development/Local**: You can often use `admin` for both `ODOO_USER` and `ODOO_PASSWORD`.
    - **Production (Odoo Online)**: The `ODOO_USER` is your email and the `ODOO_PASSWORD` is your API Key (Go to My Profile -> Account Security -> New API Key).
    - **Master Password**: In some setups (like Docker or local installs), you also need an `ODOO_MASTER_PASSWORD`. This is used for database management tasks (creating/deleting databases) and is set during the initial Odoo setup.
    - ⚠️ **CRITICAL**: Store this password in a safe place. If you forget it, you will lose the ability to manage your Odoo databases through the web interface, as it is not easily recoverable.

---

## 🚀 Installation & Usage

1. **Clone the Project**:
   ```bash
   git clone <repository-url>
   cd Gold_Tier
   ```

2. **Setup Virtual Environment**:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure `.env`**:
   Create a `.env` file based on the keys mentioned in the **Credential Guide** section. (Use `.env.example` if provided).

4. **Run the System**:
   ```powershell
   # Run once to process current tasks
   python run_system.py

   # Run in continuous loop mode (The "AI Employee" mode)
   python run_system.py --loop
   ```

---

## 🛠 Troubleshooting

- **Twitter Login Loop**: If you see "Please try again later", wait 15 minutes. Twitter has flagged the IP for too many login attempts.
- **Emoji Error**: If ChromeDriver crashes on emojis, the system is now configured to skip non-BMP characters. Emojis will be stripped to ensure the post completes.
- **Element Intercepted**: If the "Post" button isn't clickable, the system automatically switches to a JavaScript-based force click.

---

## 📈 Future Benefits
- **Scale**: Add more watchers (e.g., Slack, Discord) without changing the core engine.
- **Audit**: The `AI_Employee_Vault` provides a 100% transparent audit log of everything the AI has done.
- **Safety**: The human-in-the-loop ensures the AI never goes "rogue" or posts something unintended.

---
*Created for the Personal AI Employee Hackathon 2026.*
