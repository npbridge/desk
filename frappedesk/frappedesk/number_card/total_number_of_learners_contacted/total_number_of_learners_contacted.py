import frappe

# whitelisted function to return total count of ticket grouped over email
@frappe.whitelist(allow_guest=True)
def get():

    value = 0 

    tickets = frappe.get_list(
        "Ticket",
        fields=["contact", "name"],
        group_by = "contact"
    )

    if not tickets:
        value = 0  

    value = len(tickets)
    
    return value
