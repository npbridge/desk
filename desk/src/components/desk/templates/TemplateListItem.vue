<template>
  <div
    class="block select-none rounded-[6px] py-[7px] px-[11px]"
    :class="selected ? 'bg-blue-50 hover:bg-blue-100' : 'hover:bg-gray-50'"
  >
    <div v-if="template" role="button" class="flex items-center text-base">
      <div class="w-[37px] h-[14px] flex items-center">
        <Input
          type="checkbox"
          @click="$emit('toggleSelect')"
          :checked="selected"
          role="button"
        />
      </div>
      <router-link
        :to="`/frappedesk/templates/${template.name}`"
        class="w-full group flex items-center"
      >
        <div class="w-3/12 truncate pr-10">
          {{ template.subject }}
        </div>
        <div v-html="template.response" class="w-7/12 truncate pr-10"></div>
        <div class="w-2/12">
          <div class="pl-2">
            <a
              :title="
                template.default_auto_reply_template ? 'default template' : ''
              "
              ><CustomIcons
                v-if="template.default_auto_reply_template"
                name="circle-check"
                class="h-[20px] w-[20px] fill-blue-500"
            /></a>
          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script>
import { Input, FeatherIcon } from 'frappe-ui'
import CustomIcons from '@/components/desk/global/CustomIcons.vue'

export default {
  name: 'TemplateListItem',
  props: ['template', 'selected'],
  components: {
    Input,
    FeatherIcon,
    CustomIcons,
  },
  computed: {
    templateFetched() {
      return this.$resources.templateFetched.data || null
    },
  },
  resources: {
    templateFetched() {
      return {
        method: 'frappedesk.api.ticket.get_template_by_name',
        params: {
          template: this.template.name,
        },
        auto: true,
      }
    },
  },
}
</script>
