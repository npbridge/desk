<template>
  <div
    v-if="user.isLoggedIn() && user.has_desk_access"
    class="w-screen h-screen"
  >
    <div v-if="initialized">
      <div class="w-screen">
        <SideBarMenu id="sidebar" class="bg-gray-50" />
        <router-view id="main" />
      </div>
    </div>
    <div v-else class="h-full w-full flex max-w-full grow-0">
      <div class="mx-auto my-auto text-base font-normal">
        <!-- insert png -->
        <img
          src="https://www.col.org/wp-content/uploads/2021/08/col-logo-stacked-color-1.png"
          class="w-[200px]"
        />
        <!-- <CustomIcons name="frappedesk" class="w-[200px]"/> -->
      </div>
    </div>
  </div>
</template>

<style>
#sidebar {
  height: 100%;
  width: 0;
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  transition: 0.5s;
  visibility: collapse;
}
#main {
  margin-left: 0px;
  transition: margin-left 0.7s;
}

@media screen and (min-width: 768px) {
  #main {
    margin-left: 241px;
  }
  #sidebar {
    width: 241px;
    visibility: visible;
  }
}
</style>

<script>
import SideBarMenu from '@/components/desk/SideBarMenu.vue'
import { inject, provide, ref } from 'vue'
import CustomIcons from '@/components/desk/global/CustomIcons.vue'

export default {
  name: 'Desk',
  components: {
    SideBarMenu,
    CustomIcons,
  },
  data() {
    return {
      mounted: false,
    }
  },
  setup() {
    const user = inject('user')

    const ticketTypes = ref([])
    const ticketTags = ref([])
    const contactCourses = ref([])
    const ticketPriorities = ref([])
    const ticketStatuses = ref([])

    const ticketController = ref({})

    const contacts = ref([])
    const contactController = ref({})

    const agents = ref([])
    const agentGroups = ref([])
    const agentController = ref({})

    const sideBarFilterMap = ref({
      all: 'All Tickets',
      'my-open-tickets': 'My Open Tickets',
      'my-replied-tickets': 'My Replied Tickets',
      'my-resolved-tickets': 'My Resolved Tickets',
      'my-closed-tickets': 'My Closed Tickets',
    })
    provide('sideBarFilterMap', sideBarFilterMap)

    const ticketSideBarFilter = ref('all')
    provide('ticketSideBarFilter', ticketSideBarFilter)

    provide('ticketTypes', ticketTypes)
    provide('ticketTags', ticketTags)
    provide('contactCourses', contactCourses)
    provide('ticketPriorities', ticketPriorities)
    provide('ticketStatuses', ticketStatuses)

    provide('ticketController', ticketController)

    provide('contacts', contacts)
    provide('contactController', contactController)

    provide('agents', agents)
    provide('agentGroups', agentGroups)
    provide('agentController', agentController)

    return {
      user,

      ticketTypes,
      ticketTags,
      contactCourses,
      ticketPriorities,
      ticketStatuses,

      ticketController,

      contacts,
      contactController,

      agents,
      agentGroups,
      agentController,
    }
  },
  computed: {
    initialized() {
      if (!this.mounted) return false
      if (!this.user.isLoggedIn()) return false
      if (!this.user.has_desk_access) return false
      if (this.$resources.frappedeskSettings.loading) return false
      if (!this.$resources.frappedeskSettings.data.initial_agent_set) {
        this.$resources.setupInitialAgent.submit()
        return false
      }
      if (
        !this.$resources.frappedeskSettings.data.initial_demo_ticket_created
      ) {
        this.$resources.createInitialDemoTicket.submit()
        return false
      }

      return true
    },
  },
  mounted() {
    if (!this.user.isLoggedIn()) {
      this.$router.push({
        name: 'DeskLogin',
        query: { route: this.$route.path },
      })
      return
    }
    if (!this.user.has_desk_access) {
      this.$router.push({ path: '/support/tickets' })
      return
    }
    this.$resources.frappedeskSettings.fetch()
    this.$resources.defaultOutgoingEmailAccount.fetch()
    ;(this.ticketController.set = (ticketId, type, ref = null) => {
      switch (type) {
        case 'type':
          return this.$resources.assignTicketType.submit({
            ticket_id: ticketId,
            type: ref,
          })
        case 'tag':
          return this.$resources.assignTicketTag.submit({
            ticket_id: ticketId,
            tag: ref,
          })
        case 'course':
          return this.$resources.assignContactCourse.submit({
            contact: ticketId,
            course: ref,
          })
        case 'status':
          return this.$resources.assignTicketStatus.submit({
            ticket_id: ticketId,
            status: ref,
          })
        case 'priority':
          return this.$resources.assignTicketPriority.submit({
            ticket_id: ticketId,
            priority: ref,
          })
        case 'contact':
          return this.$resources.updateTicketContact.submit({
            ticket_id: ticketId,
            contact: ref,
          })
        case 'contact_notes':
          return this.$resources.updateContactNotes.submit({
            contact: ticketId,
            notes: ref,
          })
        case 'agent':
          return this.$resources.assignTicketToAgent.submit({
            ticket_id: ticketId,
            agent_id: ref,
          })
        case 'group':
          return this.$resources.assignTicketGroup.submit({
            ticket_id: ticketId,
            agent_group: ref,
          })
        case 'notes':
          return this.$resources.setTicketNotes.submit({
            ticket_id: ticketId,
            notes: ref,
          })
      }
    }),
      (this.ticketController.new = (type, values) => {
        switch (type) {
          case 'ticket':
            return this.$resources.createTicket.submit({
              values,
            })
          case 'type':
            this.$resources.createTicketType.submit({
              type: values,
            })
            break
          case 'tag':
            this.$resources.createTicketTag.submit({
              tag: values,
            })
            break
          case 'course':
            this.$resources.createContactCourse.submit({
              course: values,
            })
            break
        }
      }),
      (this.ticketController.delete = (ticketId, type, values) => {
        switch (type) {
          case 'tag':
            return this.$resources.deleteTicketTag.submit({
              ticket_id: ticketId,
              tag: values,
            })
          case 'course':
            return this.$resources.deleteContactCourse.submit({
              contact: ticketId,
              course: values,
            })
        }
      })
    this.$socket.on('list_update', (data) => {
      switch (data.doctype) {
        case 'Ticket Type':
          this.$resources.types.reload()
          break
        case 'Contact':
          this.$resources.contacts.reload()
          break
        case 'Agent':
          this.$resources.agents.reload()
          break
      }
    })

    this.mounted = true
  },
  unmounted() {
    this.$socket.off('list_update')
  },
  resources: {
    setupInitialAgent() {
      return {
        method: 'frappedesk.api.setup.initial_agent_setup',
        onSuccess: (res) => {
          this.$router.go()
        },
        onError: (err) => {
          this.$toast({
            title: 'Something went wrong.',
            text: 'Please try again later.',
            customIcon: 'circle-fail',
            appearance: 'danger',
          })
        },
      }
    },
    createInitialDemoTicket() {
      return {
        method: 'frappedesk.api.setup.create_initial_demo_ticket',
        onSuccess: (res) => {
          this.$resources.frappedeskSettings.fetch()
        },
        onError: (err) => {
          this.$toast({
            title: 'Something went wrong.',
            text: 'Please try again later.',
            customIcon: 'circle-fail',
            appearance: 'danger',
          })
        },
      }
    },
    setHelpdeskName() {
      return {
        method: 'frappedesk.api.settings.update_helpdesk_name',
        onSuccess: (res) => {
          document.title = `FrappeDesk ${res ? ` | ${res}` : ''}`
          this.$toast({
            title: 'Helpdesk name updated!!',
            customIcon: 'circle-check',
            appearance: 'success',
          })
        },
        onError: (error) => {},
      }
    },
    skipHelpdeskNameSetup() {
      return {
        method: 'frappedesk.api.settings.skip_helpdesk_name_setup',
      }
    },
    frappedeskSettings() {
      return {
        method: 'frappe.client.get',
        params: {
          doctype: 'Frappe Desk Settings',
          name: 'Frappe Desk Settings',
        },
        onSuccess: (data) => {
          if (
            !data.initial_helpdesk_name_setup_skipped &&
            data.helpdesk_name == ''
          ) {
            this.$toast({
              title: 'Setup Helpdesk Name',
              form: {
                inputs: [
                  {
                    type: 'text',
                    fieldname: 'helpdesk_name',
                    placeholder: 'eg: FDESK',
                  },
                ],
                onSubmit: (values) => {
                  if (values.helpdesk_name) {
                    this.$resources.setHelpdeskName.submit({
                      name: values.helpdesk_name,
                    })
                  }
                },
              },
              fixed: true,
              appearance: 'info',
              position: 'bottom-right',
              onClose: () => {
                this.$resources.skipHelpdeskNameSetup.submit()
              },
            })
          }
        },
        onError: (error) => {
          this.$toast({
            title: 'Something went wrong.',
            text: 'Please try again later.',
            customIcon: 'circle-fail',
            appearance: 'danger',
          })
        },
      }
    },
    defaultOutgoingEmailAccount() {
      return {
        method: 'frappe.client.get_list',
        params: {
          doctype: 'Email Account',
          filters: [
            ['use_imap', '=', 1],
            ['IMAP Folder', 'append_to', '=', 'Ticket'],
            ['default_outgoing', '=', 1],
          ],
        },
        onSuccess: (data) => {
          if (data.length == 0) {
            this.$toast({
              title: 'Default outgoing email account not added',
              text: 'Please add a default outgoing email account in settings.',
              appearance: 'info',
              icon: 'info',
              iconClasses: 'stroke-blue-500 stroke-2',
              fixed: true,
              position: 'bottom-right',
              action: {
                title: 'Setup now',
                onClick: () => {
                  this.$clearToasts()
                  this.$router.push({ name: 'Emails' })
                },
              },
            })
          } else {
            this.$resources.agentCount.fetch()
          }
        },
        onError: (error) => {},
      }
    },
    agentCount() {
      return {
        method: 'frappe.client.get_count',
        params: {
          doctype: 'Agent',
        },
        onSuccess: (count) => {
          if (count <= 1) {
            this.$toast({
              title: 'Add agents',
              text: 'Please add a agents from settings.',
              appearance: 'info',
              icon: 'info',
              iconClasses: 'stroke-blue-500 stroke-2',
              fixed: true,
              position: 'bottom-right',
              action: {
                title: 'Add now',
                onClick: () => {
                  this.$clearToasts()
                  this.$router.push({ name: 'Agents' })
                },
              },
            })
          }
        },
        onError: (error) => {},
      }
    },
    createTicket() {
      return {
        method: 'frappedesk.api.ticket.create_new',
        onSuccess: () => {
          this.$router.go()
        },
        onError: (error) => {
          // TODO:
        },
      }
    },
    updateTicketContact() {
      return {
        method: 'frappedesk.api.ticket.update_contact',
        onSuccess: async (ticket) => {
          // TODO:
        },
        onError: (error) => {
          // TODO:
        },
      }
    },
    updateContactNotes() {
      return {
        method: 'frappedesk.api.ticket.update_contact_notes',
        onSuccess: async (contact) => {
          // TODO:
        },
        onError: (error) => {
          // TODO:
        },
      }
    },
    types() {
      return {
        method: 'frappe.client.get_list',
        params: {
          doctype: 'Ticket Type',
          pluck: 'name',
        },
        auto: this.user.has_desk_access,
        onSuccess: (data) => {
          this.ticketTypes = data
        },
        onError: (error) => {
          // TODO:
        },
      }
    },
    tags() {
      return {
        method: 'frappe.client.get_list',
        params: {
          doctype: 'Helpdesk Tag',
          fields: ['name', 'description'],
        },
        auto: this.user.has_desk_access,
        onSuccess: (data) => {
          this.ticketTags = data
        },
        onError: (error) => {
          // TODO:
        },
      }
    },
    courses() {
      return {
        method: 'frappe.client.get_list',
        params: {
          doctype: 'Course',
          fields: ['name', 'title', 'description'],
        },
        auto: this.user.has_desk_access,
        onSuccess: (data) => {
          this.contactCourses = data
        },
        onError: (error) => {
          // TODO:
        },
      }
    },
    priorities() {
      return {
        method: 'frappe.client.get_list',
        params: {
          doctype: 'Ticket Priority',
        },
        auto: this.user.has_desk_access,
        onSuccess: (data) => {
          this.ticketPriorities = data
        },
        onError: (error) => {
          // TODO:
        },
      }
    },
    statuses() {
      return {
        method: 'frappedesk.api.ticket.get_all_ticket_statuses',
        auto: this.user.has_desk_access,
        onSuccess: (data) => {
          this.ticketStatuses = data
        },
        onError: (error) => {
          // TODO:
        },
      }
    },
    contacts() {
      return {
        method: 'frappe.client.get_list',
        params: {
          doctype: 'Contact',
          fields: ['*'],
          limit_page_length: 0,
        },
        auto: this.user.has_desk_access,
        onSuccess: (data) => {
          this.contacts = data
        },
        onError: (error) => {
          // TODO:
        },
      }
    },
    agents() {
      return {
        method: 'frappe.client.get_list',
        params: {
          doctype: 'Agent',
          fields: [
            'name',
            'agent_name',
            // TODO: 'user.user_image'
          ],
          limit_page_length: 0,
        },
        auto: this.user.has_desk_access,
        onSuccess: (data) => {
          this.agents = data
        },
        onError: (error) => {
          // TODO:
        },
      }
    },
    agentGroups() {
      return {
        method: 'frappe.client.get_list',
        params: {
          doctype: 'Agent Group',
        },
        auto: this.user.has_desk_access,
        onSuccess: (data) => {
          this.agentGroups = data
        },
        onError: (error) => {
          // TODO:
        },
      }
    },
    assignTicketToAgent() {
      return {
        method: 'frappedesk.api.ticket.assign_ticket_to_agent',
        onSuccess: async () => {
          this.$event.emit('update_ticket_list')
        },
        onError: (error) => {
          // TODO:
        },
      }
    },
    assignTicketType() {
      return {
        method: 'frappedesk.api.ticket.assign_ticket_type',
        onSuccess: async (ticket) => {},
        onError: (error) => {
          // TODO:
        },
      }
    },
    assignTicketTag() {
      return {
        method: 'frappedesk.api.ticket.assign_ticket_tag',
        onSuccess: async (ticket) => {},
        onError: (error) => {
          // TODO:
        },
      }
    },
    assignContactCourse() {
      return {
        method: 'frappedesk.api.ticket.assign_contact_course',
        onSuccess: async (contact) => {},
        onError: (error) => {
          // TODO:
        },
      }
    },
    deleteTicketTag() {
      return {
        method: 'frappedesk.api.ticket.delete_ticket_tag',
        onSuccess: async (ticket) => {},
        onError: (error) => {},
      }
    },
    deleteContactCourse() {
      return {
        method: 'frappedesk.api.ticket.delete_contact_course',
        onSuccess: async (contact) => {},
        onError: (error) => {},
      }
    },
    assignTicketStatus() {
      return {
        method: 'frappedesk.api.ticket.assign_ticket_status',
        onSuccess: async () => {
          this.$event.emit('update_ticket_list')
        },
        onError: (error) => {
          // TODO:
        },
      }
    },
    assignTicketPriority() {
      return {
        method: 'frappedesk.api.ticket.assign_ticket_priority',
        onSuccess: async (ticket) => {},
        onError: (error) => {
          // TODO:
        },
      }
    },
    assignTicketGroup() {
      return {
        method: 'frappedesk.api.ticket.assign_ticket_group',
        onSuccess: async (ticket) => {},
        onError: (error) => {
          // TODO:
        },
      }
    },
    createTicketType() {
      return {
        method: 'frappedesk.api.ticket.check_and_create_ticket_type',
        onSuccess: () => {
          this.$resources.types.fetch()
        },
        onError: (error) => {
          // TODO:
        },
      }
    },
    createTicketTag() {
      return {
        method: 'frappedesk.api.ticket.check_and_create_ticket_tag',
        onSuccess: () => {
          this.$resources.tags.fetch()
        },
        onError: (error) => {
          // TODO:
        },
      }
    },
    createContactCourse() {
      return {
        method: 'frappedesk.api.ticket.check_and_create_contact_course',
        onSuccess: () => {
          this.$resources.courses.fetch()
        },
        onError: (error) => {
          // TODO:
        },
      }
    },
    setTicketNotes() {
      return {
        method: 'frappedesk.api.ticket.set_ticket_notes',
        onSuccess: async (ticket) => {},
        onError: (error) => {},
      }
    },
  },
  directivs: {},
}
</script>
