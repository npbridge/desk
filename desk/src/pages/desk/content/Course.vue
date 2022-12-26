<template>
  <div class="flex flex-col">
    <div class="flex">
      <router-link
        :to="{
          path: '/frappedesk/courses',
        }"
        class="h-[20px] mx-[10px] mt-[26px] text-[12px] text-gray-600 stroke-gray-600 flex flex-row items-center hover:text-gray-700 hover:stroke-gray-700 select-none"
        role="button"
      >
        <FeatherIcon name="arrow-left" class="w-[13px] h-[13px]" />
        <div>Back to All Courses</div>
      </router-link>
    </div>
    <div class="flex border-b h-[52px] px-[24px] shrink-0">
      <div class="grow my-auto text-[16px] font-semibold text-gray-900">
        Courses
      </div>
    </div>

    <div class="flex flex-col md:flex-row w-full h-full">
      <CourseInfo
        class="shrink-0 border-r border-[#F4F5F6]"
        :course="courseId"
      />
    </div>
  </div>
</template>

<script>
import CourseInfo from '@/components/desk/courses/CourseInfo.vue'
import { FeatherIcon } from 'frappe-ui'

export default {
  name: 'Course',
  props: ['courseId'],
  components: {
    CourseInfo,
    FeatherIcon,
  },
}
</script>
