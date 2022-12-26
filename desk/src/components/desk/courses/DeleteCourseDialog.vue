<template>
  <div>
    <Dialog :options="{ title: 'Delete Course' }" v-model="open">
      <template #body-content>
        <div class="space-y-4">
          <div class="space-y-1">Are you sure you want to delete?</div>

          <div class="flex float-right space-x-2">
            <Button appearance="danger" @click="deleteCourse">Delete</Button>
          </div>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script>
import { Input, Dialog } from 'frappe-ui'
import { computed } from 'vue'

export default {
  name: 'DeleteCourseDialog',
  props: ['modelValue', 'courses'],
  setup(props, { emit }) {
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
    }
  },
  resources: {
    deleteCourse() {
      return {
        method: 'frappe.client.delete',
        onSuccess(data) {
          this.$emit('courseDeleted', data)
          this.$router.go()
        },
        onError(err) {
          this.$toast({
            title:
              'Error deleting course, make sure course is not linked with any contact',
            customIcon: 'circle-fail',
            appearance: 'danger',
          })
        },
      }
    },
  },
  components: {
    Input,
    Dialog,
  },
  methods: {
    deleteCourse() {
      if (this.courses) {
        for (const course in this.courses) {
          let doc = {
            doctype: 'Course',
            name: course,
          }

          this.$resources.deleteCourse.submit(doc)
        }
      }
    },
  },
}
</script>

<style></style>
