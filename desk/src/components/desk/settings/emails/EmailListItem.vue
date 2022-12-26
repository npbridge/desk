<template>
  <div
    class="block select-none rounded-[6px] py-[7px] px-[11px]"
    :class="selected ? 'bg-blue-50 hover:bg-blue-100' : 'hover:bg-gray-50'"
  >
    <div v-if="emailAccount" class="flex items-center text-base">
      <div class="w-[37px] h-[14px] flex items-center">
        <Input
          type="checkbox"
          @click="$emit('toggleSelect')"
          :checked="selected"
          role="button"
        />
      </div>
      <div class="w-full group flex items-center">
        <router-link
          :to="`/frappedesk/settings/emails/${emailAccount.name}`"
          class="md:w-4/12 w-1/1"
        >
          {{ emailAccount.name }}
        </router-link>
        <div class="md:w-5/12 hidden md:block">
          {{ emailAccount.email_id }}
        </div>
        <div class="md:w-5/12 hidden md:block">
          {{ emailAccount.service }}
        </div>
        <div class="md:w-3/12 hidden md:block">
          <div class="pl-4">
            <a :title="emailAccount.default_incoming ? 'default incoming' : ''"
              ><CustomIcons
                v-if="emailAccount.enable_incoming"
                name="circle-check"
                class="h-[20px] w-[20px] fill-blue-500"
            /></a>
          </div>
        </div>
        <div class="md:w-3/12 hidden md:block">
          <div class="pl-4">
            <a :title="emailAccount.default_outgoing ? 'default outging' : ''"
              ><CustomIcons
                v-if="emailAccount.enable_outgoing"
                name="circle-check"
                class="h-[20px] w-[20px] fill-blue-500"
            /></a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Input, FeatherIcon } from 'frappe-ui'
import CustomIcons from '@/components/desk/global/CustomIcons.vue'

export default {
  name: 'EmailListItem',
  props: ['emailAccount', 'selected'],
  components: {
    Input,
    FeatherIcon,
    CustomIcons,
  },
}
</script>
