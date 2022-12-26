<template>
  <div>
    <Dialog :options="{ title: 'Delete Template' }" v-model="open">
      <template #body-content>
        <div class="space-y-4">
          <div class="space-y-1">Are you sure you want to delete?</div>

          <div class="flex float-right space-x-2">
            <Button appearance="danger" @click="deleteTemplate">Delete</Button>
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
  name: 'DeleteTemplateDialog',
  props: ['modelValue', 'templates'],
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
    deleteTemplate() {
      return {
        method: 'frappe.client.delete',
        onSuccess(data) {
          this.$emit('templateDeleted', data)
          this.$router.go()
        },
        onError(err) {
          this.$toast({
            title:
              'Error deleting template, make sure template is not default.',
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
    deleteTemplate() {
      if (this.templates) {
        for (const template in this.templates) {
          let doc = {
            doctype: 'Email Template',
            name: template,
          }

          this.$resources.deleteTemplate.submit(doc)
        }
      }
    },
  },
}
</script>

<style></style>
