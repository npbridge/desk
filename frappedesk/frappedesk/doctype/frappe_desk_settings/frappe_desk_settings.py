# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

from frappe.model.document import Document

MAXIMUM_THRESHOLD_LIMIT = 100
MINIMUM_THRESHOLD_LIMIT = 0

class FrappeDeskSettings(Document):
	
	def before_save(self):
		self.setup_complete = self.initial_agent_set and self.initial_demo_ticket_created

		if self.threshold_limit:
			if self.threshold_limit > MAXIMUM_THRESHOLD_LIMIT:
				frappe.throw(f"Threshold limit cannot be greater than {MAXIMUM_THRESHOLD_LIMIT}")
			elif self.threshold_limit < MINIMUM_THRESHOLD_LIMIT:
				frappe.throw(f"Threshold limit cannot be less than {MINIMUM_THRESHOLD_LIMIT}")
