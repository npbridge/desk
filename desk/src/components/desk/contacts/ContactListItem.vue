<template>
  <div
    class="block select-none rounded-[6px] py-[7px] px-[11px]"
    :class="selected ? 'bg-blue-50 hover:bg-blue-100' : 'hover:bg-gray-50'"
  >
    <div v-if="contact" role="button" class="flex items-center text-base">
      <div class="w-[37px] h-[14px] flex items-center">
        <Input
          type="checkbox"
          @click="$emit('toggleSelect')"
          :checked="selected"
          role="button"
        />
      </div>
      <router-link
        :to="`/frappedesk/contacts/${contact.name}`"
        class="w-full group flex items-center"
      >
        <div class="w-3/5 md:w-5/12 truncate pr-10">
          {{ fullName }}
        </div>
        <div class="md:w-6/12 truncate pr-10 hidden md:block">
          <div v-if="contact.email && contact.email.length > 0">
            {{ contact.email[0] }}
          </div>
        </div>
        <div class="w-2/5 md:w-3/12 truncate pr-10">
          <div v-if="contactFetched">
            <div
              v-if="contactFetched.course.length > 0"
              class="flex flex-row shrink-0 flex-wrap"
            >
              <div v-for="course in contactFetched.course" :key="course">
                <div
                  class="bg-white border px-[8px] rounded-[10px] h-fit w-fit border-[black] text-[black] mr-[0.2rem] mb-[0.2rem]"
                >
                  <div
                    class="flex flex-row items-center h-[20px] space-x-[7px]"
                  >
                    <div class="text-[10px] uppercase grow">
                      {{
                        contactCourses.find(
                          (ccourse) => ccourse.name === course.course
                        )?.title
                      }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script>
import { computed, ref } from 'vue'
import { Input, FeatherIcon } from 'frappe-ui'

export default {
  name: 'ContactListItem',
  props: ['contact', 'selected'],
  components: {
    Input,
    FeatherIcon,
  },
  setup(props) {
    const fullName = computed(() => {
      if (props.contact) {
        return (
          (props.contact.first_name || '') +
          ' ' +
          (props.contact.last_name || '')
        )
      }
    })
    const contactCourses = ref([])

    return {
      fullName,
      contactCourses,
    }
  },
  computed: {
    contactFetched() {
      return this.$resources.contactFetched.data || null
    },
  },
  resources: {
    contactFetched() {
      return {
        method: 'frappedesk.api.ticket.get_contact_by_name',
        params: {
          contact: this.contact.name,
        },
        auto: true,
      }
    },
    courses() {
      return {
        method: 'frappe.client.get_list',
        params: {
          doctype: 'Course',
          fields: ['name', 'description'],
        },
        auto: true,
        onSuccess: (data) => {
          this.contactCourses = data
        },
        onError: (error) => {
          // TODO:
        },
      }
    },
  },
}
</script>
