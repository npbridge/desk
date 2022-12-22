<template>
  <div
    class="block select-none rounded-[6px] py-[7px] px-[11px]"
    :class="selected ? 'bg-blue-50 hover:bg-blue-100' : 'hover:bg-gray-50'"
  >
    <div v-if="tag" role="button" class="flex items-center text-base">
      <div class="w-[37px] h-[14px] flex items-center">
        <Input
          type="checkbox"
          @click="$emit('toggleSelect')"
          :checked="selected"
          role="button"
        />
      </div>
      <router-link
        :to="`/frappedesk/tags/${tag.name}`"
        class="w-full group flex items-center"
      >
        <div class="w-1/1 truncate pr-10">
          {{ tag.description }}
        </div>
      </router-link>
    </div>
  </div>
</template>

<script>
import { Input, FeatherIcon } from 'frappe-ui'

export default {
  name: 'TagListItem',
  props: ['tag', 'selected'],
  components: {
    Input,
    FeatherIcon,
  },
  computed: {
    tagFetched() {
      return this.$resources.tagFetched.data || null
    },
  },
  resources: {
    tagFetched() {
      return {
        method: 'frappedesk.api.ticket.get_tag_by_name',
        params: {
          tag: this.tag.name,
        },
        auto: true,
      }
    },
  },
}
</script>
