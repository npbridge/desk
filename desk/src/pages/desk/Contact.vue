<template>
  <div class="flex flex-col">
    <div class="flex">
      <router-link
        :to="{
          path: '/frappedesk/contacts',
        }"
        class="h-[20px] mx-[10px] mt-[26px] text-[12px] text-gray-600 stroke-gray-600 flex flex-row items-center hover:text-gray-700 hover:stroke-gray-700 select-none"
        role="button"
      >
        <FeatherIcon name="arrow-left" class="w-[13px] h-[13px]" />
        <div>Back to All Contacts</div>
      </router-link>
    </div>
    <div class="flex border-b h-[52px] px-[24px] shrink-0">
      <div class="grow my-auto text-[16px] font-semibold text-gray-900">
        Contacts
      </div>
    </div>

    <div class="flex flex-col md:flex-row w-full h-full">
      <ContactInfo
        class="shrink-0 border-r border-[#F4F5F6]"
        :contact="contactId"
      />
      <ContactRelatedInfo class="grow" :contact="contactId" />
    </div>
  </div>
</template>

<script>
import ContactInfo from '@/components/desk/contacts/ContactInfo.vue'
import ContactRelatedInfo from '@/components/desk/contacts/ContactRelatedInfo.vue'
import { FeatherIcon } from 'frappe-ui'

export default {
  name: 'Contact',
  props: ['contactId'],
  components: {
    ContactInfo,
    ContactRelatedInfo,
    FeatherIcon,
  },
}
</script>
