import sys
import json
import datetime
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Odoo JSON-RPC Client for Gold Tier
# Connects to Odoo 19+ Community Edition

class OdooClient:
    def __init__(self):
        self.url = os.getenv("ODOO_URL", "http://localhost:8069")
        self.db = os.getenv("ODOO_DB", "odoo")
        self.username = os.getenv("ODOO_USER", "admin")
        self.password = os.getenv("ODOO_PASSWORD", "admin")
        self.uid = None

    def _call(self, service, method, *args):
        endpoint = f"{self.url}/jsonrpc"
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": service,
                "method": method,
                "args": args
            },
            "id": 1
        }
        try:
            response = requests.post(endpoint, json=payload, timeout=10)
            response.raise_for_status()
            res = response.json()
            if "error" in res:
                raise Exception(f"Odoo Error: {res['error']}")
            return res.get("result")
        except Exception as e:
            print(f"[Odoo] Connection Error: {e}")
            return None

    def authenticate(self):
        print(f"[*] Authenticating with Odoo at {self.url}...")
        self.uid = self._call("common", "authenticate", self.db, self.username, self.password, {})
        return self.uid

    def execute(self, model, method, *args, **kwargs):
        if not self.uid:
            if not self.authenticate():
                return None
        return self._call("object", "execute_kw", self.db, self.uid, self.password, model, method, args, kwargs)

    def create_invoice(self, partner_name, amount, description):
        print(f"[*] Creating invoice for {partner_name} (Amount: {amount})...")
        
        # 1. Find or Create Partner
        partner_ids = self.execute("res.partner", "search", [["name", "=", partner_name]])
        if not partner_ids:
            partner_id = self.execute("res.partner", "create", {"name": partner_name})
        else:
            partner_id = partner_ids[0]

        # 2. Create Invoice (account.move in Odoo 13+)
        # Simplified for Gold Tier Hackathon
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': partner_id,
            'invoice_date': datetime.date.today().isoformat(),
            'invoice_line_ids': [
                (0, 0, {
                    'name': description,
                    'quantity': 1,
                    'price_unit': float(amount),
                })
            ]
        }
        
        invoice_id = self.execute("account.move", "create", invoice_vals)
        if invoice_id:
            # Optionally post/validate the invoice
            # self.execute("account.move", "action_post", [invoice_id])
            print(f"[✓] Invoice created successfully: ID {invoice_id}")
            return invoice_id
        return None

    def get_weekly_summary(self):
        summary = {
            "total_invoiced": 0.0,
            "pending_payments": 0.0,
            "new_customers": 0,
            "count": 0,
            "status": "Real Data from Audit Logs"
        }
        
        if not os.path.exists(LOG_FILE):
            return summary
            
        try:
            customers = set()
            with open(LOG_FILE, "r") as f:
                for line in f:
                    entry = json.loads(line)
                    if entry.get("action") == "create_invoice" and entry.get("status") == "SUCCESS":
                        details = entry.get("details", {})
                        amount = float(details.get("amount", 0))
                        summary["total_invoiced"] += amount
                        summary["count"] += 1
                        if "partner" in details:
                            customers.add(details["partner"])
            
            summary["new_customers"] = len(customers)
            summary["pending_payments"] = summary["total_invoiced"] # Assuming not paid yet
        except Exception as e:
            print(f"[!] Summary Error: {e}")
            
        return summary

LOG_FILE = os.path.join(os.path.dirname(__file__), "odoo_audit.log")

def log_action(action, details, status="SUCCESS"):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "action": action,
        "details": details,
        "status": status
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    client = OdooClient()
    
    if len(sys.argv) < 2:
        print("Usage: python odoo_server.py <action> [args...]")
        sys.exit(1)

    action = sys.argv[1]
    
    if action == "create_invoice":
        if len(sys.argv) < 5:
            print("Error: Missing arguments for create_invoice (partner, amount, desc)")
            log_action("create_invoice", "Missing args", "FAILED")
        else:
            partner = sys.argv[2]
            amount = sys.argv[3]
            desc = sys.argv[4]
            res = client.create_invoice(partner, amount, desc)
            if res:
                log_action("create_invoice", {"partner": partner, "amount": amount, "invoice_id": res})
            else:
                log_action("create_invoice", {"partner": partner, "amount": amount}, "FAILED")
            
    elif action == "audit":
        summary = client.get_weekly_summary()
        if summary:
            print(json.dumps(summary, indent=2))
        else:
            # Return mock if Odoo connection fails for demonstration
            print(json.dumps({
                "total_invoiced": 0.0,
                "pending_payments": 0.0,
                "new_customers": 0,
                "status": "Odoo Offline - Showing 0s"
            }, indent=2))
        
    else:
        print(f"Unknown action: {action}")
