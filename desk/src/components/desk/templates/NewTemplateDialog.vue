<template>
  <div>
    <Dialog :options="{ title: 'Create New Template' }" v-model="open">
      <template #body-content>
        <div class="space-y-4">
          <div class="space-y-1">
            <Input label="Template Name" type="text" v-model="templateName" />
            <ErrorMessage :message="templateNameValidationError" />
          </div>
          <div class="space-y-1">
            <label class="block mb-2 text-sm leading-4 text-gray-700"
              >Response</label
            >
            <CustomTextEditor
              :show="true"
              :content="response"
              editorClasses="w-full min-h-[120px] max-h-[500px] bg-gray-100 px-3 rounded-t-lg"
              @change="
                (val) => {
                  response = val
                }
              "
            >
              <template #bottom-section="{ editor }">
                <div
                  class="p-1 select-none flex flex-row border-b border-x rounded-b-lg"
                >
                  <div class="w-full flex flex-row items-center space-x-2">
                    <div
                      v-for="item in [
                        'bold',
                        'italic',
                        '|',
                        'quote',
                        'code',
                        '|',
                        'numbered-list',
                        'bullet-list',
                        'left-align',
                        'center-align',
                        'right-align',
                      ]"
                      :key="item"
                    >
                      <TextEditorMenuItem :item="item" :editor="editor" />
                    </div>
                  </div>
                </div>
              </template>
            </CustomTextEditor>
            <ErrorMessage :message="responseValidationError" />
          </div>
          <div class="space-y-1">
            <div class="flex flex-row space-x-5">
              <div class="block mt-1 text-sm leading-4 text-gray-700">
                Default
              </div>
              <CustomSwitch v-model="defaultTemplate" />
            </div>
          </div>

          <div class="flex float-right space-x-2">
            <Button
              :loading="this.$resources.createTemplate.loading"
              appearance="primary"
              @click="createTemplate()"
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
import CustomTextEditor from '@/components/global/CustomTextEditor.vue'
import CustomSwitch from '@/components/global/CustomSwitch.vue'
import TextEditorMenuItem from '@/components/global/TextEditorMenuItem.vue'

export default {
  name: 'NewTemplateDialog',
  props: {
    modelValue: {
      type: Boolean,
      required: true,
    },
  },
  setup(props, { emit }) {
    const templateNameValidationError = ref('')
    const responseValidationError = ref('')

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
      templateNameValidationError,
      responseValidationError,
      open,
    }
  },
  data() {
    return {
      templateName: '',
      response: '',
      defaultTemplate: 0,
    }
  },
  watch: {
    templateName(newValue) {
      this.validateTemplateName(newValue)
    },
    response(newValue) {
      this.validateResponse(newValue)
    },
  },
  resources: {
    createTemplate() {
      return {
        method: 'frappe.client.insert',
        onSuccess(data) {
          this.template = ''

          this.$emit('templateCreated', data)
          this.$router.go()
        },
      }
    },
  },
  components: {
    Input,
    Dialog,
    ErrorMessage,
    CustomTextEditor,
    CustomSwitch,
    TextEditorMenuItem,
  },
  methods: {
    createTemplate() {
      if (this.validateInputs()) {
        return
      }

      let doc = {
        doctype: 'Email Template',
        subject: this.templateName,
        response: this.response,
        default_auto_reply_template: this.defaultTemplate,
      }

      this.$resources.createTemplate.submit({
        doc,
      })
    },
    validateInputs() {
      let error = this.validateTemplateName(this.templateName)
      error += this.validateResponse(this.response)
      return error
    },
    validateTemplateName(value) {
      this.templateNameValidationError = ''
      if (!value) {
        this.templateNameValidationError = 'Template name should not be empty'
      } else if (value.trim() == '') {
        this.templateNameValidationError = 'Template name should not be empty'
      }
      return this.templateNameValidationError
    },
    validateResponse(value) {
      this.responseValidationError = ''
      if (!value) {
        this.responseValidationError = 'Response should not be empty'
      } else if (value.trim() == '') {
        this.responseValidationError = 'Response should not be empty'
      }
      return this.responseValidationError
    },
  },
}
</script>

<style></style>
