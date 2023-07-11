<template>
  <div>
    <Dialog :options="{ title: 'Create New Contact' }" v-model="open">
      <template #body-content>
        <div class="space-y-4">
          <div class="space-y-1">
            <Input label="First Name" type="text" v-model="firstName" />
            <ErrorMessage :message="firstNameValidationError" />
          </div>
          <div class="space-y-1">
            <div
              class="flex flex-row justify-between text-gray-600 font-normal text-[12px]"
            >
              <div class="text-gray-600">Course</div>
            </div>
            <Autocomplete
              v-if="contactCourses"
              :options="
                contactCourses.map((x) => {
                  return { label: x.name, value: x.name }
                })
              "
              placeholder="Assign courses"
              :value="course"
              @change="
                (item) => {
                  item && item.value && (course = item.value)
                }
              "
            >
              <template #input>
                <div class="flex flex-row space-x-1 items-center w-full">
                  <div class="grow">
                    <div
                      v-if="course"
                      class="text-base text-left text-black-400"
                    >
                      {{ course }}
                    </div>
                    <div v-else class="text-base text-left text-gray-400">
                      courses
                    </div>
                  </div>
                </div>
              </template>
              <!-- <template #no-result-found>
								<div 
									role="button" 
									class="hover:bg-gray-100 px-2.5 py-1.5 rounded-md text-base text-blue-500 font-semibold"
									@click="() => {
										this.openCreateNewContactCourseDialog = true
									}"
								>
									Create new
								</div>
							</template> -->
            </Autocomplete>
            <ErrorMessage :message="courseValidationError" />
          </div>
          <div class="space-y-1">
            <Input
              label="Last Name (optional)"
              type="text"
              v-model="lastName"
            />
            <ErrorMessage :message="lastNameValidationError" />
          </div>
          <div class="space-y-1">
            <Input label="Email Id" type="email" v-model="emailId" />
            <ErrorMessage :message="emailValidationError" />
          </div>
          <!-- <div class="space-y-1"> -->

          <!-- </div> -->
          <div class="flex float-right space-x-2">
            <Button
              :loading="this.$resources.createContact.loading"
              appearance="primary"
              @click="createContact()"
              >Create</Button
            >
          </div>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script>
import { Input, Dialog, ErrorMessage } from 'frappe-ui'
import { computed, ref, inject } from 'vue'
import Autocomplete from '@/components/global/Autocomplete.vue'

export default {
  name: 'NewContactDialog',
  props: {
    modelValue: {
      type: Boolean,
      required: true,
    },
  },
  setup(props, { emit }) {
    const emailValidationError = ref('')
    const firstNameValidationError = ref('')
    const lastNameValidationError = ref('')
    const courseValidationError = ref('')

    const contacts = inject('contacts')
    const contactCourses = inject('contactCourses')

    let open = computed({
      get: () => props.modelValue,
      set: (val) => {
        emit('update:modelValue', val)
        if (!val) {
          emit('close')
        }
      },
    })

    return {
      open,
      contacts,
      emailValidationError,
      firstNameValidationError,
      lastNameValidationError,
      courseValidationError,
      contactCourses,
    }
  },
  data() {
    return {
      firstName: '',
      lastName: '',
      emailId: '',
      course: '',
    }
  },
  watch: {
    emailId(newValue) {
      this.validateEmailInput(newValue)
    },
    firstName(newValue) {
      this.validateFirstName(newValue)
    },
    course(newValue) {
      this.validateCourse(newValue)
    },
  },
  resources: {
    createContact() {
      return {
        method: 'frappe.client.insert',
        onSuccess(data) {
          this.emailId = ''
          this.firstName = ''
          this.lastName = ''
          this.course = ''

          this.$emit('contactCreated', data)
          this.$router.go()
        },
      }
    },
  },
  components: {
    Input,
    Dialog,
    ErrorMessage,
    Autocomplete,
  },
  methods: {
    createContact() {
      if (this.validateInputs()) {
        return
      }

      let doc = {
        doctype: 'Contact',
        first_name: this.firstName,
        last_name: this.lastName,
        email_ids: [{ email_id: this.emailId, is_primary: true }],
        course: [{ course: this.course }],
      }

      this.$resources.createContact.submit({
        doc,
      })
    },
    coursesAsDropdownOptions() {
      let options = []
      let coursesOptions = []
      this.contactCourses.forEach((course) => {
        coursesOptions.push({
          label: course.title,
          handler: () => {
            this.course = course.name
          },
        })
      })
      options.push({
        group: 'All Courses',
        hideLabel: true,
        items: coursesOptions,
      })
      return options
    },
    validateInputs() {
      let error = this.validateEmailInput(this.emailId)
      error += this.validateFirstName(this.firstName)
      error += this.validateCourse(this.course)
      return error
    },
    validateEmailInput(value) {
      function existingContactEmails(contacts) {
        let list = []
        for (let index in contacts) {
          list.push(contacts[index].email_id)
        }
        return list
      }

      this.emailValidationError = ''
      const reg =
        /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,24}))$/
      if (!value) {
        this.emailValidationError = 'Email should not be empty'
      } else if (!reg.test(value)) {
        this.emailValidationError = 'Enter a valid email'
      } else if (existingContactEmails(this.contacts).includes(value)) {
        this.emailValidationError = 'Contact with email already exists'
      }
      return this.emailValidationError
    },
    validateFirstName(value) {
      this.firstNameValidationError = ''
      if (!value) {
        this.firstNameValidationError = 'First name should not be empty'
      } else if (value.trim() == '') {
        this.firstNameValidationError = 'First name should not be empty'
      }
      return this.firstNameValidationError
    },
    validateCourse(value) {
      this.courseValidationError = ''
      if (!value) {
        this.courseValidationError = 'Enter a valid course'
      }
      return this.courseValidationError
    },
  },
}
</script>

<style></style>
