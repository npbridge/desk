<template>
	<div class="pt-[20px] h-full flex flex-col" v-if="ticket">
		<div
			class="shrink-0 text-base px-[16px] pb-[17px]"
			:class="editingContact ? '' : 'border-b'"
		>
			<LoadingText v-if="updatingContact" />
			<div v-else>
				<div v-if="!editingContact">
					<div v-if="ticket.contact" class="space-y-[12px]">
						<div class="flex flex-row items-center space-x-[12px]">
							<div class="w-7">
								<CustomAvatar
									:label="contactFullName"
									:imageURL="ticket.contact.image"
									size="md"
								/>
							</div>
							<a
								:title="contactFullName"
								class="grow truncate font-normal text-base"
								>{{ contactFullName }}</a
							>
							<div class="flex">
								<FeatherIcon
									name="edit-2"
									class="stroke-slate-400 w-4 h-4 cursor-pointer"
									@click="
										() => {
											editingContact = !editingContact
										}
									"
								/>
							</div>
						</div>
						<div class="flex flex-col space-y-[8px]">
							<div class="flex flex-row justify-between text-gray-600 font-normal text-[12px]">
								<div class="text-gray-600">Courses</div>
							</div>
						<div v-if="ticket.contact.course.length > 0 " class="flex flex-row shrink-0 flex-wrap">
							<div v-for="course in ticket.contact.course" :key="course">
								<div 
								class="bg-white border px-[8px] rounded-[10px] h-fit w-fit border-[black] text-[black] mr-[0.2rem] mb-[0.2rem]" 
									>
									<div class="flex flex-row items-center h-[20px] space-x-[7px]">
										<div class="text-[10px] uppercase grow">{{ course.course }} </div>
											<div>
												<FeatherIcon name="x-circle" class="h-3 stroke-black-500  cursor-pointer" @click="removeCourse(course.name)" />
											</div>
									</div>
								</div>
							</div>
						</div>
						<Autocomplete 
						v-if="contactCourses"
						:options="contactCourses.map(x => {
							return {label: x.name , value: x.name}
						})"
						placeholder="Set courses"
						:value="ticket.contact.course.length > 0  ? ticket.contact.course[0].name : ''" 
						@change="(item) => {
							if (item.value) {
								ticketController.set(ticket.contact.name, 'course', item.value).then(() => {
									$resources.ticket.fetch()
	
									$toast({
										title: 'Ticket updated successfully.',
										customIcon: 'circle-check',
										appearance: 'success',
									})
								})
							}
						}"
							>
							<template #input>
								<div class="flex flex-row space-x-1 items-center w-full">
									<div class="grow">
										<div class="text-base text-left text-gray-400"> courses </div>
									</div>
								</div>
							</template>
							<template #no-result-found>
								<div 
									role="button" 
									class="hover:bg-gray-100 px-2.5 py-1.5 rounded-md text-base text-blue-500 font-semibold"
									@click="() => {
										this.openCreateNewContactCourseDialog = true
									}"
								>
									Create new
								</div>
							</template>
						</Autocomplete>
						</div> 
						<div
							v-if="ticket.contact.phone_nos.length > 0"
							class="flex space-x-[12px] items-center"
							>
							<FeatherIcon
								name="phone"
								class="stroke-gray-500"
								style="width: 15px"
							/>
							<div
								class="space-y-1"
								v-for="phone_no in ticket.contact.phone_nos"
								:key="phone_no"
							>
								<a :title="phone_no.phone" class="text-gray-700 text-base">{{
									phone_no.phone
								}}</a>
							</div>
						</div>
						<div
							v-if="ticket.contact.email_ids.length > 0"
							class="flex space-x-[12px] items-center"
							>
							<FeatherIcon
								name="mail"
								class="stroke-gray-500"
								style="width: 15px"
							/>
							<div
								class="space-y-1 max-w-[173px]"
								v-for="email in ticket.contact.email_ids"
								:key="email"
							>
								<div
									:title="email.email_id"
									class="truncate text-gray-700 text-base"
								>
									<a :title="email.email_id">{{ email.email_id }}</a>
								</div>
							</div>
						</div>
						<div class="flex flex-row items-center space-x-[12px]">
							<Input label="Notes" type="textarea" :value="contactNotes" class="text-gray-600" @change="updateNotes" />
						</div> 
					</div>
					<div v-else>
						<div v-if="!updatingContact" class="flex flex-row-reverse">
							<FeatherIcon
								name="edit-2"
								class="stroke-slate-400 w-4 h-4 cursor-pointer"
								@click="
									() => {
										editingContact = !editingContact
									}
								"
							/>
						</div>
					</div>
				</div>
				<div v-else class="w-full">
					<div class="flex space-x-2 mb-2">
						<div class="grow">Select Contact</div>
						<FeatherIcon
							name="x"
							class="stroke-slate-400 w-4 h-4 cursor-pointer hover:stroke-red-500"
							@click="
								() => {
									editingContact = !editingContact
								}
							"
						/>
					</div>
					<Combobox v-model="selectedContact">
						<ComboboxInput
							class="rounded-md w-full border-none focus:ring-0 py-2 pl-3 pr-10 text-sm leading-5 text-gray-900 bg-slate-100"
							autocomplete="off"
							@change="query = $event.target.value"
						/>
						<ComboboxOptions
							class="w-full py-1 mt-1 overflow-auto text-base bg-white rounded-md shadow-lg max-h-60 ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
						>
							<div
								v-if="filterdContacts.length === 0 && query !== ''"
								class="select-none relative py-2 px-4 text-gray-700 cursor-pointer"
								@click="
									() => {
										showNewContactDialog = true
									}
								"
							>
								Create new
							</div>
							<ComboboxOption
								v-slot="{ selected, active }"
								v-for="contactItem in filterdContacts"
								:key="contactItem"
								:value="contactItem.name"
							>
								<li
									class="cursor-default select-none relative py-2 pl-4 pr-4 text-gray-900"
									:class="{ 'bg-slate-50': active }"
								>
									<span
										class="block truncate"
										:class="{
											'font-medium': selected,
											'font-normal': !selected,
										}"
									>
										{{ contactItem.name }}
									</span>
								</li>
							</ComboboxOption>
						</ComboboxOptions>
					</Combobox>
				</div>
			</div>
		</div>
		<div class="grow" v-if="!editingContact">
			<div class="h-full flex flex-col">
				<div
					class="p-[16px] border-t border-b"
					v-if="ticket.custom_fields.length > 0"
				>
					<!-- <div class="text-gray-700 text-sm">{{ `more info ${ticket.template != 'Default' ? `(${ticket.template})` : ''}` }}</div> -->
					<div class="space-y-[12px] text-[12px]">
						<div class="space-y-[12px]">
							<div
								class="flex flex-col space-y-[8px] font-normal hover:underline"
								v-for="field in ticket.custom_fields.filter((field) => {
									return field.is_action_field == '1'
								})"
								:key="field.fieldname"
							>
								<a :title="field.value" :href="field.route" target="_blank">{{
									field.label
								}}</a>
							</div>
						</div>
						<div class="space-y-[12px]">
							<div
								class="flex flex-col space-y-[8px] font-normal"
								v-for="field in ticket.custom_fields.filter((field) => {
									return field.is_action_field != '1'
								})"
								:key="field.fieldname"
							>
								<div class="text-gray-600">{{ field.label }}</div>
								<div
									v-if="field.route"
									class="w-fit flex flex-row items-center space-x-[12px] cursor-pointer hover:underline"
								>
									<FeatherIcon
										name="external-link"
										class="w-[14px] h-[14px] stroke-gray-500"
									/>
									<div class="w-[200px] truncate">
										<a
											:title="field.value"
											class="text-gray-900 text-base"
											:href="field.route"
											target="_blank"
											>{{ field.value }}</a
										>
									</div>
								</div>
								<div v-else>
									<div class="flex flex-row items-center space-x-[12px]">
										<FeatherIcon
											name="info"
											class="w-[14px] h-[14px] stroke-gray-500"
										/>
										<div class="w-[200px] truncate">
											<a
												:title="field.value"
												class="text-gray-900 text-base w-[200px]"
												>{{ field.value }}</a
											>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div
					class="shrink-0 border-b p-[16px] space-y-1 select-none"
					v-if="otherTicketsOfContact"
				>
					<div
						class="flex flex-row items-center"
						:class="otherTicketsOfContact.length > 0 ? 'cursor-pointer' : ''"
						@click="
							() => {
								showOtherTicketsOfContacts = !showOtherTicketsOfContacts
							}
						"
					>
						<div class="grow text-gray-600 text-[11px] font-semibold">
							OPEN TICKETS ({{ otherTicketsOfContact.length }})
						</div>
						<FeatherIcon
							v-if="otherTicketsOfContact.length > 0"
							class="h-[15px] w-[15px] stroke-gray-500"
							:name="showOtherTicketsOfContacts ? 'chevron-up' : 'chevron-down'"
						/>
					</div>
					<div
						v-if="
							showOtherTicketsOfContacts && otherTicketsOfContact.length > 0
						"
						class="overflow-scroll pt-[4px] space-y-[4px] text-gray-700 font-normal"
					>
						<div
							v-for="(_ticket, index) in otherTicketsOfContact"
							:key="_ticket.name"
							:set="(maxCount = 5)"
						>
							<router-link
								v-if="index <= maxCount"
								:to="
									index < maxCount
										? `/frappedesk/tickets/${_ticket.name}`
										: `/frappedesk/tickets/?contact=${ticket.contact.name}&menu_filter=all&page=1`
								"
								class="text-[12px] rounded"
							>
								<div class="py-[1px]">
									<div
										v-if="index < maxCount"
										class="flex flex-row space-x-[12px] items-center hover:bg-gray-100"
									>
										<div class="w-[15px] h-[15px]">
											<FeatherIcon
												name="arrow-up-right"
												class="w-[15px] h-[15px] stroke-gray-500"
											/>
										</div>
										<div class="max-w-[180px]">
											<div class="truncate">
												<a class="text-[12px]" :title="_ticket.subject">{{
													_ticket.subject
												}}</a>
											</div>
										</div>
									</div>
									<div
										v-else
										class="hover:text-gray-600 flex flex-row-reverse text-[11px]"
									>
										View all
									</div>
								</div>
							</router-link>
						</div>
					</div>
				</div>
				<div class="h-full">
					<div
						class="flex flex-col p-[16px] select-none"
						:class="showTicketHistory ? '' : 'border-b'"
					>
						<div
							class="shrink-0 flex flex-row items-center cursor-pointer"
							@click="
								() => {
									showTicketHistory = !showTicketHistory
								}
							"
						>
							<div class="grow text-gray-600 text-[11px] font-semibold">
								TICKET HISTORY
							</div>
							<FeatherIcon
								class="h-[15px] w-[15px] stroke-gray-500"
								:name="showTicketHistory ? 'chevron-up' : 'chevron-down'"
							/>
						</div>
						<div
							v-if="showTicketHistory"
							class="overflow-y-scroll"
							:style="{
								height:
									viewportWidth > 768
										? `calc(100vh - ${getOffsetHeight}px)`
										: null,
							}"
						>
							<Activities :ticketId="ticket.name" />
						</div>
					</div>
				</div>
			</div>
		</div>
		<NewContactDialog
			v-model="showNewContactDialog"
			@contact-created="
				(contact) => {
					contactCreated(contact)
				}
			"
		/>
		<Dialog :options="{title: 'Create New Course'}" v-model="openCreateNewContactCourseDialog">
			<template #body-content>
				<div class="space-y-4">
					<Input type="text" v-model="newCourse" placeholder="eg: Course-1" />
					<div class="flex float-right space-x-2">
						<Button @click="createAndAssignContactCourseFromDialog()">Create and Assign</Button>
						<Button @click="createContactCourseFromDialog()" appearance="primary">Create</Button>
					</div>
				</div>
			</template>
		</Dialog>
	</div>
</template>

<script>
import { FeatherIcon, Input, LoadingText } from 'frappe-ui'
import CustomAvatar from '@/components/global/CustomAvatar.vue'
import CustomIcons from '@/components/desk/global/CustomIcons.vue'
import Activities from '@/components/desk/ticket/Activities.vue'
import {
	Combobox,
	ComboboxInput,
	ComboboxOptions,
	ComboboxOption,
} from '@headlessui/vue'
import NewContactDialog from '@/components/desk/global/NewContactDialog.vue'
import { inject, ref } from 'vue'
import Autocomplete from '@/components/global/Autocomplete.vue'


export default {
	name: 'InfoPanel',
	props: ['ticketId'],
	components: {
		FeatherIcon,
		Input,
		LoadingText,
		CustomAvatar,
		CustomIcons,
		Activities,
		Combobox,
		ComboboxInput,
		ComboboxOption,
		ComboboxOptions,
		NewContactDialog,
		Autocomplete
	},
	data() {
		return {
			openCreateNewContactCourseDialog: false,
			newCourse: "",
		}
	},
	setup() {
		const viewportWidth = inject('viewportWidth')
		const editingContact = ref(false)
		const updatingContact = ref(false)
		const contactName = ref('')
		const selectedContact = ref('')
		const query = ref('')

		const showNewContactDialog = ref(false)
		const showTicketHistory = ref(false)

		const contacts = inject('contacts')
		const ticketController = inject('ticketController')

		const contactCourses = inject('contactCourses')

		const showOtherTicketsOfContacts = ref(false)

		return {
			viewportWidth,
			editingContact,
			updatingContact,
			contactName,
			selectedContact,
			query,
			showNewContactDialog,
			showTicketHistory,
			contacts,
			ticketController,
			showOtherTicketsOfContacts,
			contactCourses
		}
	},
	computed: {
		ticket() {
			return this.$resources.ticket.data || null
		},
		contactFullName() {
			if (this.ticket.contact) {
				return (
					(this.ticket.contact.first_name || '') +
					' ' +
					(this.ticket.contact.last_name || '')
				).slice(0, 40)
			}
		},
		contactNotes(){
			if (this.ticket.contact) { 
				return this.ticket.contact.notes || ''
			}
		},
		filterdContacts() {
			return this.query === ''
				? this.contacts
				: this.contacts.filter((contactItem) => {
						return contactItem.name
							.toLowerCase()
							.includes(this.query.toLowerCase())
					})
		},
		otherTicketsOfContact() {
			return this.$resources.otherTicketsOfContact.data || null
		},
		getOffsetHeight() {
			const offset = 290
			const multiplier = 30
			const maxCount = 5

			const customFiledWidth = 34
			const customFieldPadding = this.ticket.custom_fields.length == 1 ? 30 : 60

			return (
				offset +
				multiplier *
					(this.showOtherTicketsOfContacts
						? this.otherTicketsOfContact.length <= maxCount
							? this.otherTicketsOfContact.length
							: maxCount
						: 0) +
				(this.ticket.custom_fields.length > 0
					? customFieldPadding * 2 +
						customFiledWidth * this.ticket.custom_fields.length
					: 0)
			)
		},
	},
	watch: {
		selectedContact(newValue) {
			if (newValue) {
				this.updateContact()
			}
		},
	},
	methods: {
		createAndAssignContactCourseFromDialog() {
			if (this.newCourse) {
				this.ticketController.set(this.ticket.contact.name, 'course', this.newCourse).then(() => {
					this.$resources.ticket.fetch()

					this.$toast({
						title: 'Ticket updated successfully.',
						customIcon: 'circle-check',
						appearance: 'success',
					})
				})
				this.closeCreateNewContactCourseDialog();
			}
		},
		createContactCourseFromDialog() {
			if (this.newCourse) {
				this.ticketController.new('course', this.newCourse)
				this.closeCreateNewContactCourseDialog();
			}
		},
		removeCourse(course){
			this.ticketController.delete(this.ticket.contact.name, 'course', course).then(() => {
				this.$resources.ticket.fetch()

				this.$toast({
					title: 'Ticket updated successfully.',
					customIcon: 'circle-check',
					appearance: 'success',
				})
			})
		}, 
		closeCreateNewContactCourseDialog() {
			this.newCourse = ""
			this.openCreateNewContactCourseDialog = false
		},
		updateNotes(note) {
			this.ticketController.set(this.ticket.contact.name, 'contact_notes', note)
		},
		updateContact() {
			this.editingContact = false
			this.updatingContact = true
			this.ticketController
				.set(this.ticketId, 'contact', this.selectedContact)
				.then(() => {
					this.selectedContact = ''
					this.query = ''
					this.updatingContact = false
					this.$resources.otherTicketsOfContact.fetch()

					this.$resources.ticket.fetch()
				})
		},
		contactCreated(contact) {
			this.showNewContactDialog = false
			this.editingContact = false
			this.ticketController.set(this.ticketId, 'contact', contact.name)
		},
	},
	resources: {
		otherTicketsOfContact() {
			return {
				cache: ['Other Tickets', 'Action Panel', this.ticketId],
				method: 'frappedesk.api.ticket.get_other_tickets_of_contact',
				params: {
					ticket_id: this.ticketId,
				},
				auto: true,
			}
		},
		ticket() {
			return {
				cache: ['Ticket', 'Action Panel', this.ticketId],
				method: 'frappedesk.api.ticket.get_ticket',
				params: {
					ticket_id: this.ticketId,
				},
				auto: true,
			}
		},
	},
}
</script>
