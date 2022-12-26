<template>
  <div>
    <div>
      <ListManager
        class="px-[16px]"
        ref="tagList"
        :options="{
          cache: ['Tags', 'Desk'],
          doctype: 'Helpdesk Tag',
          fields: ['name', 'description'],
          limit: 40,
          start_page: initialPage,
          route_query_pagination: true,
        }"
      >
        <template #body="{ manager }">
          <div>
            <div class="flow-root py-4 px-[16px]">
              <div class="text-right mb-3">
                <SidebarCollapserVue />
              </div>
              <div class="float-left"></div>
              <div class="float-right">
                <div class="flex items-center space-x-3">
                  <div
                    class="stroke-blue-500 fill-blue-500 w-0 h-0 block"
                  ></div>
                  <Button
                    icon-left="plus"
                    appearance="primary"
                    @click="
                      () => {
                        showNewTagDialog = true
                      }
                    "
                    >Add Tag</Button
                  >
                  <Button
                    v-if="Object.keys(manager.selectedItems).length > 0"
                    icon-left="x"
                    appearance="danger"
                    @click="
                      () => {
                        showConfirmDeleteDialog = true
                        tagsToDelete = manager.selectedItems
                      }
                    "
                    >{{
                      Object.keys(manager.selectedItems).length > 1
                        ? 'Delete Tags'
                        : 'Delete Tag'
                    }}
                  </Button>
                </div>
              </div>
            </div>
            <TagList :manager="manager" />
          </div>
        </template>
      </ListManager>
    </div>
    <NewTagDialog
      v-model="showNewTagDialog"
      @tag-created="
        () => {
          showNewTagDialog = false
        }
      "
    />
    <DeleteTagDialog
      v-model="showConfirmDeleteDialog"
      :tags="tagsToDelete"
      @tag-deleted="
        () => {
          showConfirmDeleteDialog = false
          tagsToDelete = null
        }
      "
    />
  </div>
</template>
<script>
import ListManager from '@/components/global/ListManager.vue'
import TagList from '@/components/desk/tags/TagList.vue'
import NewTagDialog from '@/components/desk/tags/NewTagDialog.vue'
import { ref } from 'vue'
import SidebarCollapserVue from '@/components/global/SidebarCollapser.vue'
import DeleteTagDialog from '@/components/desk/tags/DeleteTagDialog.vue'

export default {
  name: 'Tags',
  components: {
    ListManager,
    NewTagDialog,
    TagList,
    SidebarCollapserVue,
    DeleteTagDialog,
  },
  data() {
    return {
      initialPage: 1,
      tagsToDelete: null,
    }
  },
  setup() {
    const showNewTagDialog = ref(false)
    const showConfirmDeleteDialog = ref(false)

    return {
      showNewTagDialog,
      showConfirmDeleteDialog,
    }
  },
  computed: {
    tags() {
      return this.tags || null
    },
  },
  mounted() {
    this.initialPage = parseInt(
      this.$route.query.page ? this.$route.query.page : 1
    )
  },
}
</script>
