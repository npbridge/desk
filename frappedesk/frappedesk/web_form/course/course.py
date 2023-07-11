import frappe

def get_context(context):
	# do your magic here
	if (context["in_edit_mode"] or context["in_view_mode"] or context.get("is_new", False)):
		context["web_form_doc"]["web_form_fields"][-1]["fields"][0]["hidden"] = True
	pass
