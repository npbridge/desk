<template>
  <div>
    <div
      class="bg-[#F7F7F7] group flex items-center text-base font-medium text-gray-500 py-[10px] pl-[11px] pr-[17px] rounded-[6px] select-none"
    >
      <div class="w-[37px] h-[14px]">
        <Input
          type="checkbox"
          @click="manager.selectAll()"
          :checked="manager.allItemsSelected"
          role="button"
        />
      </div>
      <div class="flex flex-row items-center group w-full">
        <div class="w-3/5 md:w-5/12">Name</div>
      </div>
    </div>
    <div
      id="rows"
      class="flex flex-col space-y-2 overflow-scroll"
      :style="{ height: viewportWidth > 768 ? 'calc(100vh - 6.4rem)' : null }"
    >
      <div v-if="!manager.loading">
        <div v-if="manager.list.length > 0">
          <div v-for="(tag, index) in manager.list" :key="tag.description">
            <TagListItem
              :class="index == 0 ? 'mt-[9px] mb-[2px]' : 'my-[2px]'"
              :tag="tag"
              @toggle-select="manager.select(tag)"
              :selected="manager.itemSelected(tag)"
            />
          </div>
        </div>
        <div v-else>
          <div class="grid place-content-center h-48 w-full">
            <div>
              <CustomIcons name="empty-list" class="h-12 w-12 mx-auto mb-2" />
              <div class="text-gray-500 mb-2">No tags found</div>
            </div>
          </div>
        </div>
      </div>
      <ListPageController :manager="manager" />
    </div>
  </div>
</template>

<script>
import { inject } from 'vue'
import { Input } from 'frappe-ui'
import TagListItem from '@/components/desk/tags/TagListItem.vue'
import CustomIcons from '@/components/desk/global/CustomIcons.vue'
import ListPageController from '@/components/global/ListPageController.vue'

export default {
  name: 'TagList',
  props: ['manager'],
  components: {
    TagListItem,
    CustomIcons,
    Input,
    ListPageController,
  },
  setup() {
    const viewportWidth = inject('viewportWidth')
    return {
      viewportWidth,
    }
  },
}
</script>

<style></style>
