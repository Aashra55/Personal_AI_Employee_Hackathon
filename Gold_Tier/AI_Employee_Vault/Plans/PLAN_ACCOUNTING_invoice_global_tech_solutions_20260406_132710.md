PLAN:
1. Extract invoice details from the TASK CONTEXT, including client, project, amount, currency, and due date.
2. Consult the `accounting` skill logic (specifically `odoo-accounting`) for preparing the invoice data.
3. Prepare the data for an `odoo_invoice` action request, ensuring all required fields are populated.
4. Include the instruction about a 10% early payment discount in the invoice description/notes.
5. Ensure the content reflects the "Digital FTE integration" project and the "Aashra's AI Employee" signature for any related email.

## ACTION_REQUEST
---
type: odoo_invoice

Client: Global Tech Solutions
Amount: 2500
Currency: USD
Project: AI Strategy & Implementation (Digital FTE integration)
Due_Date: 14 days from 2026-04-06

## Content
Invoice for the final phase of the Digital FTE integration.
Note: Include a 10% discount for early payment.
Email Signature: Aashra's AI Employee
---
