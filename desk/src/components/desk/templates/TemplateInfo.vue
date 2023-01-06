<template>
  <div class="min-w-[304px] px-[24px] py-[10px]">
    <div class="form w-full flex flex-col">
      <div class="flex flex-col space-y-[24px]">
        <Input
          class="grow"
          label="Template Name"
          type="text"
          :value="values?.subject"
          @change="(val) => (values.subject = val)"
        />
        <label class="block mb-2 text-sm leading-4 text-gray-700"
          >Response</label
        >
        <CustomTextEditor
          :show="true"
          :content="values?.response"
          editorClasses="w-full min-h-[120px] max-h-[500px] bg-gray-100 px-3 rounded-t-lg"
          @change="
            (val) => {
              values.response = val
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
        <div class="flex flex-row space-x-5">
          <div class="block mt-1 text-sm leading-4 text-gray-700">Default</div>
          <CustomSwitch v-model="values.defaultTemplate" />
        </div>
        <div class="w-full flex flex-row">
          <div>
            <Button @click="cancel()">Cancel</Button>
          </div>
          <div class="grow flex flex-row-reverse">
            <Button
              :loading="this.$resources.template.setValue.loading"
              appearance="primary"
              @click="save()"
              >Save</Button
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { FeatherIcon, Input } from 'frappe-ui'
import CustomAvatar from '@/components/global/CustomAvatar.vue'
import Autocomplete from '@/components/global/Autocomplete.vue'
import CustomTextEditor from '@/components/global/CustomTextEditor.vue'
import CustomSwitch from '@/components/global/CustomSwitch.vue'
import TextEditorMenuItem from '@/components/global/TextEditorMenuItem.vue'

export default {
  name: 'TemplateInfo',
  props: ['template'],
  components: {
    FeatherIcon,
    Input,
    CustomAvatar,
    Autocomplete,
    CustomTextEditor,
    CustomSwitch,
    TextEditorMenuItem,
  },
  computed: {
    templateDoc() {
      return this.$resources.template.doc || null
    },
    values() {
      if (this.$resources.template.setValue.loading) {
        return this.values || null
      }
      return {
        subject: this.templateDoc ? this.templateDoc.subject : null,
        response: this.templateDoc ? this.templateDoc.response : null,
        defaultTemplate: this.templateDoc
          ? this.templateDoc.default_auto_reply_template
          : null,
      }
    },
  },

  resources: {
    template() {
      return {
        type: 'document',
        doctype: 'Email Template',
        name: this.template,
        setValue: {
          onSuccess: () => {
            this.$toast({
              title: 'Template Updated.',
              customIcon: 'circle-check',
              appearance: 'success',
            })
          },
          onError: (error) => {
            this.$toast({
              title:
                'Error in updating. Make sure you have a default template.',
              customIcon: 'circle-fail',
              appearance: 'error',
            })
          },
        },
      }
    },
  },
  methods: {
    save() {
      this.$resources.template.setValue.submit({
        subject: this.values.subject,
        response: this.values.response,
        default_auto_reply_template: this.values.defaultTemplate,
      })
    },
    cancel() {
      this.$router.push({ name: 'Templates' })
    },
  },
}
</script>

<style></style>
