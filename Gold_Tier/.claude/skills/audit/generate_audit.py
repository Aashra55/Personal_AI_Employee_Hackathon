import os
import datetime
import json

def generate_ceo_briefing():
    print("[*] Compiling Weekly CEO Briefing...")
    
    # Paths to log files
    odoo_log = "../../mcp_server/odoo_audit.log"
    social_log = "../../mcp_server/social_audit.log"
    
    # Summary logic
    report_content = f"# Weekly CEO Briefing - {datetime.date.today()}\n\n"
    
    report_content += "## 💰 Financial Summary (Odoo)\n"
    if os.path.exists(odoo_log):
        with open(odoo_log, "r") as f:
            lines = f.readlines()[-5:] # Last 5 transactions
            report_content += "".join([f"- {line}" for line in lines])
    else:
        report_content += "No recent financial transactions found.\n"
        
    report_content += "\n## 📱 Social Media Summary\n"
    if os.path.exists(social_log):
        with open(social_log, "r") as f:
            lines = f.readlines()[-5:] # Last 5 posts
            report_content += "".join([f"- {line}" for line in lines])
    else:
        report_content += "No recent social media activity found.\n"

    # Save report
    report_dir = "../../AI_Employee_Vault/Archive/Reports"
    os.makedirs(report_dir, exist_ok=True)
    report_path = f"{report_dir}/CEO_BRIEFING_{datetime.date.today().strftime('%Y%m%d')}.md"
    
    with open(report_path, "w") as f:
        f.write(report_content)
        
    return {"status": "success", "report": report_path}

if __name__ == "__main__":
    result = generate_ceo_briefing()
    print(json.dumps(result))
