<template>
  <div>
    <Dialog :options="{ title: 'Delete Tag' }" v-model="open">
      <template #body-content>
        <div class="space-y-4">
          <div class="space-y-1">Are you sure you want to delete?</div>

          <div class="flex float-right space-x-2">
            <Button appearance="danger" @click="deleteTag">Delete</Button>
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
  name: 'DeleteTagDialog',
  props: ['modelValue', 'tags'],
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
    deleteTag() {
      return {
        method: 'frappe.client.delete',
        onSuccess(data) {
          this.$emit('tagDeleted', data)
          this.$router.go()
        },
        onError(err) {
          this.$toast({
            title:
              'Error deleting tag, make sure tag is not linked with any ticket',
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
    deleteTag() {
      if (this.tags) {
        for (const tag in this.tags) {
          let doc = {
            doctype: 'Helpdesk Tag',
            name: tag,
          }

          this.$resources.deleteTag.submit(doc)
        }
      }
    },
  },
}
</script>

<style></style>
