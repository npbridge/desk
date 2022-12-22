<template>
  <div>
    <div>
      <ListManager
        class="px-[16px]"
        ref="templateList"
        :options="{
          cache: ['Templates', 'Desk'],
          doctype: 'Email Template',
          fields: [
            'name',
            'subject',
            'response',
            'default_auto_reply_template',
          ],
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
                        showNewTemplateDialog = true
                      }
                    "
                    >Add Template</Button
                  >
                  <Button
                    v-if="Object.keys(manager.selectedItems).length > 0"
                    icon-left="x"
                    appearance="danger"
                    @click="
                      () => {
                        showConfirmDeleteDialog = true
                        templatesToDelete = manager.selectedItems
                      }
                    "
                    >{{
                      Object.keys(manager.selectedItems).length > 1
                        ? 'Delete Templates'
                        : 'Delete Template'
                    }}
                  </Button>
                </div>
              </div>
            </div>
            <TemplateList :manager="manager" />
          </div>
        </template>
      </ListManager>
    </div>
    <NewTemplateDialog
      v-model="showNewTemplateDialog"
      @template-created="
        () => {
          showNewTemplateDialog = false
        }
      "
    />
    <DeleteTemplateDialog
      v-model="showConfirmDeleteDialog"
      :templates="templatesToDelete"
      @template-deleted="
        () => {
          showConfirmDeleteDialog = false
          templatesToDelete = null
        }
      "
    />
  </div>
</template>
<script>
import ListManager from '@/components/global/ListManager.vue'
import TemplateList from '@/components/desk/templates/TemplateList.vue'
import NewTemplateDialog from '@/components/desk/templates/NewTemplateDialog.vue'
import { ref } from 'vue'
import SidebarCollapserVue from '@/components/global/SidebarCollapser.vue'
import DeleteTemplateDialog from '@/components/desk/templates/DeleteTemplateDialog.vue'

export default {
  name: 'Templates',
  components: {
    ListManager,
    NewTemplateDialog,
    TemplateList,
    SidebarCollapserVue,
    DeleteTemplateDialog,
  },
  data() {
    return {
      initialPage: 1,
      templatesToDelete: null,
    }
  },
  setup() {
    const showNewTemplateDialog = ref(false)
    const showConfirmDeleteDialog = ref(false)

    return {
      showNewTemplateDialog,
      showConfirmDeleteDialog,
    }
  },
  computed: {
    templates() {
      return this.templates || null
    },
  },
  mounted() {
    this.initialPage = parseInt(
      this.$route.query.page ? this.$route.query.page : 1
    )
  },
}
</script>
