import json
import frappe

from frappe.website.utils import cleanup_page_name
from frappedesk.frappedesk.doctype.ticket_activity.ticket_activity import log_ticket_activity
from frappedesk.frappedesk.doctype.ticket.ticket import create_communication_via_contact, get_all_conversations, create_communication_via_agent

@frappe.whitelist(allow_guest=True)
def get_ticket(ticket_id):
	ticket_doc = frappe.get_doc("Ticket", ticket_id)
	ticket_doc = ticket_doc.__dict__
	ticket_doc['assignees'] = get_agent_assigned_to_ticket(ticket_id)
	ticket_doc['contact'] = get_contact(ticket_id)
	
	return ticket_doc

@frappe.whitelist(allow_guest=True)
def create_new(values, template='Default', attachments=[], via_customer_portal=False):
	ticket_doc = frappe.new_doc("Ticket")
	ticket_doc.via_customer_portal = via_customer_portal

	if 'contact' in values:
		contact_doc = frappe.get_doc("Contact", values['contact'])
		if contact_doc.email_ids and len(contact_doc.email_ids) > 0:
			ticket_doc.raised_by = contact_doc.email_ids[0].email_id
			ticket_doc.contact = contact_doc.name

	if via_customer_portal:
		if not frappe.db.exists({"doctype": "Contact", "email_id": frappe.session.user}):
			user_doc = frappe.get_doc("User", frappe.session.user)
			new_contact_doc = frappe.get_doc(
				doctype="Contact", 
				email_id=user_doc.email,
				full_name=user_doc.full_name,
				first_name=user_doc.first_name,
				last_name=user_doc.last_name,
				user=user_doc.name
			)
			new_contact_doc.append("email_ids", {"email_id": user_doc.email, "is_primary": True})
			new_contact_doc.insert(ignore_permissions=True)
			ticket_doc.contact = new_contact_doc.name

	ticket_doc.subject = values['subject']
	ticket_doc.description = values['description']

	ticket_doc.template = template
	template_fields = frappe.get_doc("Ticket Template", template).fields
	for field in template_fields:
		if field.fieldname in ['subject', 'description']:
			continue
		if field.auto_set and field.auto_set_via == 'Backend (Python)':
			continue
		else:
			ticket_doc.append('custom_fields', {
				'label': field.label,
				'fieldname': field.fieldname,
				'value': values[field.fieldname],
				'route': f'/app/{cleanup_page_name(field.options)}/{values[field.fieldname]}' if field.fieldtype == 'Link' else '',
				'is_action_field': field.is_action_field
			})

	ticket_doc.insert(ignore_permissions=True)
	# TODO: remove this if condition after refactoring doctype/ticket.py logic regarding this
	create_communication_via_contact(ticket_doc.name, ticket_doc.description, attachments)
	# if not via_customer_portal:

	return ticket_doc

@frappe.whitelist(allow_guest=True)
def update_contact(ticket_id, contact):
	if ticket_id:
		ticket_doc = frappe.get_doc("Ticket", ticket_id)
		contact_doc = frappe.get_doc("Contact", contact)
		if contact_doc.email_ids and len(contact_doc.email_ids) > 0:
			ticket_doc.raised_by = contact_doc.email_ids[0].email_id
			ticket_doc.contact = contact_doc.name

		ticket_doc.save()
		
		return ticket_doc

@frappe.whitelist(allow_guest=True)
def update_contact_notes(contact, notes):
	if contact:
		contact_doc = frappe.get_doc("Contact", contact)
		if notes and contact_doc.notes != notes:
			contact_doc.notes = notes
			contact_doc.save()

		return contact_doc

def get_agent_assigned_to_ticket(ticket_id):
	agents = []
	assignee_list = frappe.db.get_value("Ticket", ticket_id, "_assign")
	if assignee_list:
		assignees = json.loads(assignee_list)

		agent = frappe.qb.DocType("Agent")
		user = frappe.qb.DocType("User")
		query = (
			frappe.qb.from_(agent)
			.join(user)
			.on(agent.name == user.name)
			.select(agent.name, agent.agent_name, agent.group, user.user_image.as_("image"))
			.where(agent.name.isin(assignees))
		)
		agents = query.run(as_dict=True)

	return agents

@frappe.whitelist()
def mark_ticket_as_seen(ticket_id):
	if ticket_id:
		return frappe.get_doc("Ticket", ticket_id).add_seen()

@frappe.whitelist(allow_guest=True)
def assign_ticket_to_agent(ticket_id, agent_id=None):
	if ticket_id:
		ticket_doc = frappe.get_doc("Ticket", ticket_id)
		
		if agent_id is None:
			# assign to self
			agent_id = frappe.session.user
			if not frappe.db.exists("Agent", agent_id):
				frappe.throw('Tickets can only assigned to agents')
		
		ticket_doc.assign_agent(agent_id)
		return ticket_doc

@frappe.whitelist(allow_guest=True)
def bulk_assign_ticket_to_agent(ticket_ids, agent_id=None):
	if ticket_ids:
		ticket_docs = []
		for ticket_id in ticket_ids:
			ticket_doc = assign_ticket_to_agent(ticket_id, agent_id)
			ticket_docs.append(ticket_doc)
		return ticket_docs

@frappe.whitelist(allow_guest=True)
def assign_ticket_type(ticket_id, type):
	if ticket_id:
		ticket_doc = frappe.get_doc("Ticket", ticket_id)
		
		if ticket_doc.ticket_type != type:
			ticket_doc.ticket_type = check_and_create_ticket_type(type).name
			ticket_doc.update_priority_based_on_ticket_type()
			ticket_doc.save()
			log_ticket_activity(ticket_id, f"type set to {type}")

		return ticket_doc

@frappe.whitelist(allow_guest=True)
def assign_ticket_tag(ticket_id, tag):
	if ticket_id:
		ticket_doc = frappe.get_doc("Ticket", ticket_id)
		if ticket_doc:
			tag_exists = False
			for ticket_tag in ticket_doc.ticket_tag:
				if ticket_tag.tag == tag:
					tag_exists = True
					break

			if not tag_exists:
				ticket_tag_doc = check_and_create_ticket_tag(tag)
				if ticket_tag_doc:
					ticket_doc.append("ticket_tag", {
							"tag": ticket_tag_doc.name,
						})
					ticket_doc.save()
					log_ticket_activity(ticket_id, f"tag: {tag} added.")

			return ticket_doc

@frappe.whitelist(allow_guest=True)
def assign_contact_course(contact, course):
	if contact:
		contact_doc = frappe.get_doc("Contact", contact)
		if contact_doc:
			course_exists = False
			for contact_course in contact_doc.course:
				if contact_course.course == course:
					course_exists = True
					break

			if not course_exists:
				contact_course_doc = check_and_create_contact_course(course)
				if contact_course_doc:
					contact_doc.append("course", {
							"course": contact_course_doc.name,
						})
					contact_doc.save()

			return contact_doc

@frappe.whitelist(allow_guest=True)
def delete_ticket_tag(ticket_id, tag):
	ticket_doc = frappe.get_doc("Ticket", ticket_id)

	row_to_delete = None
	for row in ticket_doc.ticket_tag:
		if row.name == tag:
			row_to_delete = row
			break

	if row_to_delete: 
		ticket_doc.remove(row) 
		ticket_doc.save()
		log_ticket_activity(ticket_id, f"tag: {tag} removed.")

	return ticket_doc

@frappe.whitelist(allow_guest=True)
def delete_contact_course(contact, course):
	contact_doc = frappe.get_doc("Contact", contact)

	row_to_delete = None
	for row in contact_doc.course:
		if row.name == course:
			row_to_delete = row
			break

	if row_to_delete: 
		contact_doc.remove(row) 
		contact_doc.save()

	return contact_doc

@frappe.whitelist(allow_guest=True)
def assign_ticket_status(ticket_id, status):
	if ticket_id:
		ticket_doc = frappe.get_doc("Ticket", ticket_id)
		
		if ticket_doc.status != status:
			ticket_doc.status = status
			ticket_doc.save(ignore_permissions=True)
			log_ticket_activity(ticket_id, f"status set to {status}")

		return ticket_doc

@frappe.whitelist(allow_guest=True)
def mark_as_unread(ticket_id):
	if ticket_id:
		ticket_doc = frappe.get_doc("Ticket", ticket_id)
		_seen = json.loads(ticket_doc._seen or "[]")
		_seen = [user for user in _seen if frappe.session.user != user]
		ticket_doc.db_set("_seen", json.dumps(_seen), update_modified=False)
		
		log_ticket_activity(ticket_id, f"Ticket marked as unread ")

		return ticket_doc

@frappe.whitelist()
def follow_ticket(ticket_id):
	if ticket_id:
		ticket_doc = frappe.get_doc("Ticket", ticket_id)
		_liked_by = json.loads(ticket_doc._liked_by or "[]")
		if frappe.session.user not in _liked_by:
			_liked_by.append(frappe.session.user)

		ticket_doc.db_set("_liked_by", json.dumps(_liked_by), update_modified=False)
		
		return ticket_doc

@frappe.whitelist()
def unfollow_ticket(ticket_id):
	if ticket_id:
		ticket_doc = frappe.get_doc("Ticket", ticket_id)
		_liked_by = json.loads(ticket_doc._liked_by or "[]")
		_liked_by = [user for user in _liked_by if frappe.session.user != user]
		ticket_doc.db_set("_liked_by", json.dumps(_liked_by), update_modified=False)
		
		return ticket_doc

@frappe.whitelist(allow_guest=True)
def set_ticket_notes(ticket_id, notes):
	if ticket_id:
		ticket_doc = frappe.get_doc("Ticket", ticket_id)
		
		if ticket_doc.notes != notes:
			ticket_doc.notes = notes
			ticket_doc.save()
			log_ticket_activity(ticket_id, f"updated notes")

		return ticket_doc


@frappe.whitelist(allow_guest=True)
def bulk_assign_ticket_status(ticket_ids, status):
	if ticket_ids:
		ticket_docs = []
		for ticket_id in ticket_ids:
			ticket_doc = assign_ticket_status(ticket_id, status)
			ticket_docs.append(ticket_doc)
		return ticket_docs

@frappe.whitelist(allow_guest=True)
def bulk_mark_as_unread(ticket_ids):
	if ticket_ids:
		ticket_docs = []
		for ticket_id in ticket_ids:
			ticket_doc = mark_as_unread(ticket_id)
			ticket_docs.append(ticket_doc)
		return ticket_docs

@frappe.whitelist()
def bulk_follow(ticket_ids):
	if ticket_ids:
		ticket_docs = []
		for ticket_id in ticket_ids:
			ticket_doc = follow_ticket(ticket_id)
			ticket_docs.append(ticket_doc)
		return ticket_docs

@frappe.whitelist(allow_guest=True)
def assign_ticket_priority(ticket_id, priority):
	if ticket_id:
		ticket_doc = frappe.get_doc("Ticket", ticket_id)
		
		if ticket_doc.priority != priority:
			ticket_doc.priority = priority
			ticket_doc.save()
			log_ticket_activity(ticket_id, f"priority set to {priority}")

		return ticket_doc

@frappe.whitelist(allow_guest=True)
def assign_ticket_group(ticket_id, agent_group):
	if ticket_id:
		ticket_doc = frappe.get_doc("Ticket", ticket_id)
		
		if ticket_doc.agent_group != agent_group:
			ticket_doc.agent_group = agent_group
			log_ticket_activity(ticket_id, f"team set to {agent_group}")
			ticket_doc.save()
		
		return ticket_doc

@frappe.whitelist(allow_guest=True)
def get_all_ticket_types():
	return frappe.get_all("Ticket Type", pluck="name")

#TODO: the code can be made better
@frappe.whitelist(allow_guest=True)
def get_all_ticket_statuses():
	statuses = []
	ticket_doctype = frappe.get_doc("DocType", "Ticket")
	for field in ticket_doctype.fields:
		doc_field = frappe.get_doc("DocField", field.__dict__["name"])
		if doc_field.label == "Status":
			statuses = doc_field.options.split("\n")
	return statuses

@frappe.whitelist(allow_guest=True)
def get_all_ticket_priorities():
	return frappe.get_all("Ticket Priority", pluck="name")

def get_contact(ticket_id):
	contact_id = frappe.get_value("Ticket", ticket_id, "contact")
	if contact_id:
		contact_doc = frappe.get_doc("Contact", contact_id)
		return contact_doc
	else:
		ticket_doc = frappe.get_doc("Ticket", ticket_id)
		if (ticket_doc.raised_by):
			ticket_doc.set_contact(ticket_doc.raised_by, True)
			contact_id = frappe.get_value("Ticket", ticket_id, "contact")
			if (contact_id):
				contact_doc = frappe.get_doc("Contact", contact_id)
				return contact_doc
	return None

@frappe.whitelist(allow_guest=True)
def get_contact_by_name(contact):
	if contact:
		contact_doc = frappe.get_doc("Contact", contact)
		return contact_doc

@frappe.whitelist(allow_guest=True)
def get_course_by_name(course):
	if course:
		course_doc = frappe.get_doc("Course", course)
		return course_doc

@frappe.whitelist(allow_guest=True)
def get_tag_by_name(tag):
	if tag:
		tag_doc = frappe.get_doc("Helpdesk Tag", tag)
		return tag_doc

@frappe.whitelist(allow_guest=True)
def get_template_by_name(template):
	if template:
		email_template_doc = frappe.get_doc("Email Template", template)
		return email_template_doc

@frappe.whitelist(allow_guest=True)
def fetch_ticket_with_tags(tags): 
	ticket_tag_doctype = frappe.get_list("Ticket Tag", fields = ['parent'], filters={'tag':('in', tags)}, parent_doctype="Ticket")
	return [tag.parent for tag in ticket_tag_doctype]

@frappe.whitelist(allow_guest=True)
def get_conversations(ticket_id):
	return get_all_conversations(ticket_id)

@frappe.whitelist(allow_guest=True)
def submit_conversation_via_agent(ticket_id, cc, bcc,  message, attachments):
	return create_communication_via_agent(
		ticket_id, 
		message, 
		cc, 
		bcc, 
		attachments, 
		template="agent_response_with_history",
        template_args={"message": message, }
		)

@frappe.whitelist(allow_guest=True)
def submit_conversation_via_contact(ticket_id, message, attachments):
	return create_communication_via_contact(ticket_id, message, attachments)

@frappe.whitelist(allow_guest=True)
def get_other_tickets_of_contact(ticket_id):
	contact = frappe.get_value("Ticket", ticket_id, "raised_by")
	tickets = frappe.get_all("Ticket", filters={"raised_by": contact, "name": ["!=", ticket_id], "status": ["not in", ["Closed", "Resolved"]]}, fields=['name', 'subject'])
	return tickets

@frappe.whitelist(allow_guest=True)
def check_and_create_ticket_type(type):
	type_doc = frappe.db.exists("Ticket Type", type)
	if not type_doc:
		ticket_type_doc = frappe.new_doc("Ticket Type")
		ticket_type_doc.name = ticket_type_doc.description = type
		ticket_type_doc.insert()
	else:
		ticket_type_doc = frappe.get_doc("Ticket Type", type)

	return ticket_type_doc

@frappe.whitelist(allow_guest=True)
def check_and_create_ticket_tag(tag):
	tag_doc = frappe.db.exists("Helpdesk Tag", tag)
	if not tag_doc:
		ticket_tag_doc = frappe.new_doc("Helpdesk Tag")
		ticket_tag_doc.name = ticket_tag_doc.description = tag
		ticket_tag_doc.insert()
	else:
		ticket_tag_doc = frappe.get_doc("Helpdesk Tag", tag)

	return ticket_tag_doc

@frappe.whitelist(allow_guest=True)
def check_and_create_contact_course(course):
	course_doc = frappe.db.exists("Course", course)
	if not course_doc:
		contact_course_doc = frappe.new_doc("Course")
		contact_course_doc.name = contact_course_doc.title = course
		contact_course_doc.insert()
	else:
		contact_course_doc = frappe.get_doc("Course", course)

	return contact_course_doc

@frappe.whitelist(allow_guest=True)
def get_all_ticket_templates():
	templates = frappe.get_all("Ticket Template")
	for index, template in enumerate(templates):
		templates[index] = frappe.get_doc("Ticket Template", template.name).__dict__
	
	return templates

@frappe.whitelist(allow_guest=True)
def activities(name):
	activities = frappe.db.sql(
		"""
		SELECT action, creation, owner
		FROM `tabTicket Activity`
		WHERE ticket = %(ticket)s
		ORDER BY creation DESC
	""",
		values={"ticket": name},
		as_dict=1,
	)

	return activities

@frappe.whitelist(allow_guest=True)
def submit_customer_feedback(ticket_id, satisfied, feedback_text):
	ticket_doc = frappe.get_doc("Ticket", ticket_id)
	ticket_doc.satisfied = satisfied
	ticket_doc.customer_feedback = feedback_text
	ticket_doc.feedback_submitted = True
	ticket_doc.save(ignore_permissions=True)
	return ticket_doc