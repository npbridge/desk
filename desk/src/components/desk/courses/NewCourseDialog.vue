<template>
  <div>
    <Dialog :options="{ title: 'Create New Course' }" v-model="open">
      <template #body-content>
        <div class="space-y-4">
          <div class="space-y-1">
            <Input label="Course Name" type="text" v-model="courseName" />
            <ErrorMessage :message="courseNameValidationError" />
          </div>

          <div class="flex float-right space-x-2">
            <Button
              :loading="this.$resources.createCourse.loading"
              appearance="primary"
              @click="createCourse()"
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
import { computed, ref } from 'vue'

export default {
  name: 'NewCourseDialog',
  props: {
    modelValue: {
      type: Boolean,
      required: true,
    },
  },
  setup(props, { emit }) {
    const courseNameValidationError = ref('')

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
      courseNameValidationError,
      open,
    }
  },
  data() {
    return {
      courseName: '',
    }
  },
  watch: {
    courseName(newValue) {
      this.validateCourseName(newValue)
    },
  },
  resources: {
    createCourse() {
      return {
        method: 'frappe.client.insert',
        onSuccess(data) {
          this.course = ''

          this.$emit('courseCreated', data)
          this.$router.go()
        },
      }
    },
  },
  components: {
    Input,
    Dialog,
    ErrorMessage,
  },
  methods: {
    createCourse() {
      if (this.validateInputs()) {
        return
      }

      let doc = {
        doctype: 'Course',
        description: this.courseName,
      }

      this.$resources.createCourse.submit({
        doc,
      })
    },
    validateInputs() {
      let error = this.validateCourseName(this.courseName)
      return error
    },
    validateCourseName(value) {
      this.courseNameValidationError = ''
      if (!value) {
        this.courseNameValidationError = 'Course name should not be empty'
      } else if (value.trim() == '') {
        this.courseNameValidationError = 'Course name should not be empty'
      }
      return this.courseNameValidationError
    },
  },
}
</script>

<style></style>
