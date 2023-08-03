<template>
  <div class="min-w-[304px] px-[24px] py-[10px]">
    <div class="form w-full flex flex-col">
      <div
        class="float-left mb-[16px]"
        @click="
          () => {
            editingName = true
            tempContactName = values.contactName
          }
        "
      >
        <div
          v-if="!editingName"
          class="flex space-x-2 items-center cursor-pointer"
        >
          <div class="font-semibold">{{ values.contactName }}</div>
          <FeatherIcon class="w-3 h-3" name="edit-2" />
        </div>
        <div v-else class="flex space-x-2 items-center">
          <Input id="contactNameInput" v-model="tempContactName" type="text" />
          <FeatherIcon
            class="w-4 h-4"
            role="button"
            name="x"
            @click="
              () => {
                editingName = false
                tempContactName = values.contactName
              }
            "
          />
        </div>
      </div>
      <div class="flex flex-col space-y-[24px]">
        <div>
          <span class="block mb-2 text-sm leading-4 text-gray-700"
            >Profile Picture</span
          >
          <div class="flex flex-row space-x-[8px] items-center">
            <!-- if user is same as contact return image else if image is not private then return image else return null -->
            <CustomAvatar
              :label="values?.contactName"
              size="2xl"
              :imageURL="values?.profilePicture"
              :imageOwner="values?.email"
            />
            <div class="flex flex-row space-x-[8px]">
              <!-- <Button>Upload new</Button>
							<Button>Remove</Button> -->
            </div>
          </div>
        </div>
        <div class="flex flex-col space-y-[8px]">
          <div
            class="flex flex-row justify-between text-gray-600 font-normal text-[12px]"
          >
            <div class="text-gray-600">Courses</div>
          </div>
          <div
            v-if="values?.course?.length > 0"
            class="flex flex-row flex-wrap"
          >
            <div v-for="course in values?.course" :key="course">
              <div
                class="bg-white border px-[8px] rounded-[10px] h-fit w-fit border-[black] text-[black] mr-[0.2rem] mb-[0.2rem]"
              >
                <div class="flex flex-row items-center h-[20px] space-x-[2px]">
                  <div class="text-[11px] uppercase grow">
                    {{
                      contactCourses.find(
                        (ccourse) => ccourse.name === course.course
                      )?.title
                    }}
                  </div>
                  <div>
                    <FeatherIcon
                      name="x-circle"
                      class="h-3 stroke-black-500 cursor-pointer"
                      @click="removeCourse(course.name)"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
          <Autocomplete
            v-if="contactCourses"
            :options="
              contactCourses.map((course) => {
                return { label: course.title, value: course.name }
              })
            "
            placeholder="Set courses"
            :value="values?.course?.length > 0 ? values.course[0].name : ''"
            @change="assignNewCourse"
          >
            <template #input>
              <div class="flex flex-row space-x-1 items-center w-full">
                <div class="grow">
                  <div class="text-base text-left text-gray-400">courses</div>
                </div>
              </div>
            </template>
            <template #no-result-found>
              <div
                role="button"
                class="hover:bg-gray-100 px-2.5 py-1.5 rounded-md text-base text-blue-500 font-semibold"
                @click="
                  () => {
                    this.openCreateNewContactCourseDialog = true
                  }
                "
              >
                Create new
              </div>
            </template>
          </Autocomplete>
        </div>

        <Input
          class="grow"
          label="E-mail"
          type="text"
          :value="values?.email"
          @change="(val) => (values.email = val)"
        />
        <Input
          class="grow"
          label="Phone"
          type="text"
          :value="values?.phone"
          @change="(val) => (values.phone = val)"
        />
        <Input
          class="grow"
          label="Notes"
          type="textarea"
          :value="values?.notes"
          @change="(val) => (values.notes = val)"
        />
        <div class="w-full flex flex-row">
          <div>
            <Button @click="cancel()">Cancel</Button>
          </div>
          <div class="grow flex flex-row-reverse">
            <Button
              :loading="this.$resources.contact.setValue.loading"
              appearance="primary"
              @click="save()"
              >Save</Button
            >
          </div>
        </div>
      </div>
    </div>
    <Dialog
      :options="{ title: 'Create New Course' }"
      v-model="openCreateNewContactCourseDialog"
    >
      <template #body-content>
        <div class="space-y-4">
          <Input type="text" v-model="newCourse" placeholder="eg: Course-1" />
          <div class="flex float-right space-x-2">
            <Button @click="createAndAssignContactCourseFromDialog()"
              >Create and Assign</Button
            >
            <Button
              @click="createContactCourseFromDialog()"
              appearance="primary"
              >Create</Button
            >
          </div>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script>
import { ref, inject } from 'vue'
import { FeatherIcon, Input } from 'frappe-ui'
import CustomAvatar from '@/components/global/CustomAvatar.vue'
import Autocomplete from '@/components/global/Autocomplete.vue'

export default {
  name: 'ContactInfo',
  props: ['contact'],
  components: {
    FeatherIcon,
    Input,
    CustomAvatar,
    Autocomplete,
  },
  data() {
    return {
      openCreateNewContactCourseDialog: false,
      newCourse: '',
    }
  },
  setup() {
    const editingName = ref(false)
    const tempContactName = ref('')
    const contactCourses = ref([])
    const user = inject('user')

    return {
      editingName,
      tempContactName,
      contactCourses,
      user,
    }
  },
  computed: {
    contactDoc() {
      return this.$resources.contact.doc || null
    },
    values() {
      if (this.$resources.contact.setValue.loading) {
        return this.values || null
      }
      this.tempContactName = this.contactDoc
        ? `${this.contactDoc?.first_name} ${
            this.contactDoc && this.contactDoc.last_name
              ? this.contactDoc.last_name
              : ''
          }`
        : null
      return {
        contactName: this.contactDoc
          ? `${this.contactDoc?.first_name} ${
              this.contactDoc && this.contactDoc.last_name
                ? this.contactDoc.last_name
                : ''
            }`
          : null,
        profilePicture: this.contactDoc?.image || null,
        firstName: this.contactDoc?.first_name || null,
        lastName: this.contactDoc?.last_name || null,
        email:
          this.contactDoc && this.contactDoc.email_ids.length > 0
            ? this.contactDoc.email_ids[0].email_id
            : null,
        phone:
          this.contactDoc && this.contactDoc.phone_nos.length > 0
            ? this.contactDoc.phone_nos[0].phone
            : null,
        course:
          this.contactDoc &&
          this.contactDoc.course &&
          this.contactDoc.course.length > 0
            ? this.contactDoc.course
            : null,
        notes: this.contactDoc?.notes || null,
      }
    },
  },
  deactivated() {
    this.resetForm()
  },
  resources: {
    assignContactCourse() {
      return {
        method: 'frappedesk.api.ticket.assign_contact_course',
        onSuccess: async (contact) => {
          this.$router.go()
        },
        onError: (error) => {
          // TODO:
        },
      }
    },
    deleteContactCourse() {
      return {
        method: 'frappedesk.api.ticket.delete_contact_course',
        onSuccess: async (contact) => {
          this.$router.go()
        },
        onError: (error) => {},
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
    courses() {
      return {
        method: 'frappe.client.get_list',
        params: {
          doctype: 'Course',
          fields: ['name', 'title', 'description'],
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
    contact() {
      return {
        type: 'document',
        doctype: 'Contact',
        name: this.contact,
        setValue: {
          onSuccess: () => {
            this.$toast({
              title: 'Contact Updated.',
              customIcon: 'circle-check',
              appearance: 'success',
            })
            this.resetForm()
          },
        },
      }
    },
  },
  methods: {
    assignNewCourse(item) {
      if (item.value) {
        this.$resources.assignContactCourse
          .submit({
            contact: this.contactDoc.name,
            course: item.value,
          })
          .then(() => {
            this.$toast({
              title: 'Contact updated successfully.',
              customIcon: 'circle-check',
              appearance: 'success',
            })
          })
      }
    },
    createAndAssignContactCourseFromDialog() {
      if (this.newCourse) {
        this.$resources.assignContactCourse
          .submit({
            contact: this.contactDoc.name,
            course: this.newCourse,
          })
          .then(() => {
            this.$toast({
              title: 'Contact updated successfully.',
              customIcon: 'circle-check',
              appearance: 'success',
            })
          })
        this.closeCreateNewContactCourseDialog()
      }
    },
    createContactCourseFromDialog() {
      if (this.newCourse) {
        this.$resources.createContactCourse.submit({
          course: this.newCourse,
        })
        this.closeCreateNewContactCourseDialog()
      }
    },
    removeCourse(course) {
      this.$resources.deleteContactCourse
        .submit({
          contact: this.contactDoc.name,
          course: course,
        })
        .then((res) => {
          this.$toast({
            title: 'Contact updated successfully.',
            customIcon: 'circle-check',
            appearance: 'success',
          })
        })
    },
    closeCreateNewContactCourseDialog() {
      this.newCourse = ''
      this.openCreateNewContactCourseDialog = false
    },
    resetForm() {
      this.editingName = false
      this.tempContactName = this.values.contactName
    },
    save() {
      let firstName = ''
      let lastName = ''
      if (this.tempContactName.split(' ').length > 1) {
        firstName = this.tempContactName.split(' ')[0]
        lastName = this.tempContactName.slice(
          firstName.length + 1,
          this.tempContactName.length
        )
      } else {
        firstName = this.tempContactName
      }
      this.$resources.contact.setValue.submit({
        first_name: firstName,
        last_name: lastName,
        email_ids: this.values.email ? [{ email_id: this.values.email }] : [],
        phone_nos: this.values.phone ? [{ phone: this.values.phone }] : [],
        notes: this.values.notes ? this.values.notes : null,
      })
    },
    cancel() {
      this.$router.push({ name: 'Contacts' })
    },
  },
}
</script>

<style></style>
