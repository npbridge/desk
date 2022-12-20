<template>
  <div class="text-right">
    <SidebarCollapserVue class="mr-6 mt-3 w-fit" />
  </div>

  <div class="flex" v-if="$route.name === 'Article'">
    <router-link
      :to="{
        path: '/frappedesk/knowledge-base',
      }"
      class="mb-3 h-[20px] mx-[10px] mt-[26px] text-[12px] text-gray-600 stroke-gray-600 flex flex-row items-center hover:text-gray-700 hover:stroke-gray-700 select-none"
      role="button"
    >
      <FeatherIcon name="arrow-left" class="w-[13px] h-[13px]" />
      <div>Back to All Articles</div>
    </router-link>
  </div>
  <div v-else><br /></div>
  <div class="w-full flex flex-row items-center px-[24px]">
    <div class="grow">
      <span class="font-semibold tex-[16px] text-gray-900">Knowledge Base</span>
    </div>
    <div class="flex flex-row items-center space-x-2">
      <div v-for="action in actions" :key="action.label">
        <div
          v-if="action.dropdown"
          class="flex flex-row items-center space-x-2 bg-blue-500 rounded-[6px] px-[10px]"
          role="button"
        >
          <div
            class="border-r border-blue-400 pr-2 text-white text-base font-normal py-[6px]"
            @click="action.handler"
          >
            {{ action.label }}
          </div>
          <Dropdown :options="action.dropdown" placement="right">
            <template v-slot="{ toggle }">
              <div class="py-[4px]" @click="toggle">
                <FeatherIcon
                  name="chevron-down"
                  class="w-4 h-4 stroke-white"
                  role="button"
                />
              </div>
            </template>
          </Dropdown>
        </div>
        <div v-else>
          <Button
            :appearance="action.appearance || 'secondary'"
            @click="action.handler"
            >{{ action.label }}</Button
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Dropdown, FeatherIcon } from 'frappe-ui'
import { ref } from '@vue/reactivity'
import SidebarCollapserVue from '../../global/SidebarCollapser.vue'

export default {
  name: 'TopNavbar',
  components: {
    Dropdown,
    FeatherIcon,
    SidebarCollapserVue,
  },
  setup() {
    const actions = ref({})

    return {
      actions,
    }
  },
  mounted() {
    const presetActions = {
      Category: [
        {
          label: 'Add article',
          handler: () => {
            this.$emit('create_new_article')
          },
          appearance: 'primary',
          dropdown: [
            {
              label: 'Add category',
              handler: () => {
                this.$event.emit('create_new_category')
              },
            },
          ],
        },
      ],
    }
    this.$event.on('toggle_navbar_actions', ({ type, actions = [] }) => {
      if (actions.length === 0) {
        this.actions = presetActions[type]
      } else {
        this.actions = actions
      }
    })
  },
  unmounted() {
    this.$event.off('toggle_navbar_actions')
  },
}
</script>
