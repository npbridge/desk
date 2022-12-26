<template>
  <div>
    <Dialog :options="{ title: 'Create New Tag' }" v-model="open">
      <template #body-content>
        <div class="space-y-4">
          <div class="space-y-1">
            <Input label="Tag Name" type="text" v-model="tagName" />
            <ErrorMessage :message="tagNameValidationError" />
          </div>

          <div class="flex float-right space-x-2">
            <Button
              :loading="this.$resources.createTag.loading"
              appearance="primary"
              @click="createTag()"
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
  name: 'NewTagDialog',
  props: {
    modelValue: {
      type: Boolean,
      required: true,
    },
  },
  setup(props, { emit }) {
    const tagNameValidationError = ref('')

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
      tagNameValidationError,
      open,
    }
  },
  data() {
    return {
      tagName: '',
    }
  },
  watch: {
    tagName(newValue) {
      this.validateTagName(newValue)
    },
  },
  resources: {
    createTag() {
      return {
        method: 'frappe.client.insert',
        onSuccess(data) {
          this.tag = ''

          this.$emit('tagCreated', data)
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
    createTag() {
      if (this.validateInputs()) {
        return
      }

      let doc = {
        doctype: 'Helpdesk Tag',
        description: this.tagName,
      }

      this.$resources.createTag.submit({
        doc,
      })
    },
    validateInputs() {
      let error = this.validateTagName(this.tagName)
      return error
    },
    validateTagName(value) {
      this.tagNameValidationError = ''
      if (!value) {
        this.tagNameValidationError = 'Tag name should not be empty'
      } else if (value.trim() == '') {
        this.tagNameValidationError = 'Tag name should not be empty'
      }
      return this.tagNameValidationError
    },
  },
}
</script>

<style></style>
