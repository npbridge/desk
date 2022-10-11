<template>
  <div
    v-if="comment"
    class="flex flex-col my-[16px] bg-[#FDF9F2] p-[10px] rounded-[6px]"
  >
    <div class="flex flex-row justify-between">
      <div class="flex flex-row items-center space-x-[8px]" v-if="user">
        <CustomAvatar
          v-if="comment.comment_by !== 'Bot'"
          :imageURL="user.user_image"
          :label="user.full_name"
          size="sm"
        />
        <div class="truncate text-[14px] font-normal max-w-[200px]">
          {{ comment.comment_by ? comment.comment_by : user.full_name }}
          <span
            class="text-[11px] text-gray-900 bg-[#FDF9F2] shadow font-normal border border-gray-400 rounded-[6px] px-[10px] py-[2px]"
            data-v-177b47bf=""
            >Comment</span
          >
        </div>
      </div>
      <div class="flex flex-row items-center space-x-[8px]" v-else>
        <div class="truncate text-[14px] font-normal max-w-[200px]">
          {{ comment.comment_by && comment.comment_by }}
          <span
            class="text-[11px] text-gray-900 bg-[#FDF9F2] shadow font-normal border border-gray-400 rounded-[6px] px-[10px] py-[2px]"
            data-v-177b47bf=""
            >Comment</span
          >
        </div>
      </div>

      <div class="text-gray-500 text-[12px]">
        {{ $dayjs.longFormating($dayjs(comment.creation).fromNow()) }}
      </div>
    </div>
    <div class="pl-[32px] pt-[6px]">
      <div class="flex flex-col">
        <div
          class="prose prose-p:my-1 text-[13px] text-gray-700"
          v-html="cleanedMessage"
        ></div>
      </div>
    </div>
  </div>
</template>

<script>
import { FeatherIcon } from 'frappe-ui'
import CustomAvatar from '@/components/global/CustomAvatar.vue'
import { remove_script_and_style } from '@/utils'

export default {
  name: 'ConversationCard',
  props: ['comment'],
  components: {
    FeatherIcon,
    CustomAvatar,
  },
  computed: {
    cleanedMessage() {
      if (this.comment?.content) {
        return remove_script_and_style(this.comment.content)
      }
      return ''
    },
    user() {
      return this.$resources.user.data || null
    },
  },
  resources: {
    user() {
      return {
        method: 'frappe.client.get',
        params: {
          doctype: 'User',
          name: this.comment?.owner,
          fields: ['*'],
        },
        auto: true,
      }
    },
  },
}
</script>

<style></style>
