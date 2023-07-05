<template>
  <div>
    <div>
      <ListManager
        class="px-[16px]"
        ref="courseList"
        :options="{
          cache: ['Courses', 'Desk'],
          doctype: 'Course',
          fields: ['name', 'title', 'description'],
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
                        showNewCourseDialog = true
                      }
                    "
                    >Add Course</Button
                  >
                  <Button
                    v-if="Object.keys(manager.selectedItems).length > 0"
                    icon-left="x"
                    appearance="danger"
                    @click="
                      () => {
                        showConfirmDeleteDialog = true
                        coursesToDelete = manager.selectedItems
                      }
                    "
                    >{{
                      Object.keys(manager.selectedItems).length > 1
                        ? 'Delete Courses'
                        : 'Delete Course'
                    }}
                  </Button>
                </div>
              </div>
            </div>
            <CourseList :manager="manager" />
          </div>
        </template>
      </ListManager>
    </div>
    <NewCourseDialog
      v-model="showNewCourseDialog"
      @course-created="
        () => {
          showNewCourseDialog = false
        }
      "
    />
    <DeleteCourseDialog
      v-model="showConfirmDeleteDialog"
      :courses="coursesToDelete"
      @course-deleted="
        () => {
          showConfirmDeleteDialog = false
          coursesToDelete = null
        }
      "
    />
  </div>
</template>
<script>
import ListManager from '@/components/global/ListManager.vue'
import CourseList from '@/components/desk/courses/CourseList.vue'
import NewCourseDialog from '@/components/desk/courses/NewCourseDialog.vue'
import { ref } from 'vue'
import SidebarCollapserVue from '@/components/global/SidebarCollapser.vue'
import DeleteCourseDialog from '@/components/desk/courses/DeleteCourseDialog.vue'

export default {
  name: 'Courses',
  components: {
    ListManager,
    NewCourseDialog,
    CourseList,
    SidebarCollapserVue,
    DeleteCourseDialog,
  },
  data() {
    return {
      initialPage: 1,
      coursesToDelete: null,
    }
  },
  setup() {
    const showNewCourseDialog = ref(false)
    const showConfirmDeleteDialog = ref(false)

    return {
      showNewCourseDialog,
      showConfirmDeleteDialog,
    }
  },
  computed: {
    courses() {
      return this.courses || null
    },
  },
  mounted() {
    this.initialPage = parseInt(
      this.$route.query.page ? this.$route.query.page : 1
    )
  },
}
</script>
