<template>
  <div class="min-w-[304px] px-[24px] py-[10px]">
    <div class="form w-full flex flex-col">
      <div class="flex flex-col space-y-[24px]">
        <Input
          class="grow"
          label="Course Name"
          type="text"
          :value="values?.description"
          @change="(val) => (values.description = val)"
        />
        <div class="w-full flex flex-row">
          <div>
            <Button @click="cancel()">Cancel</Button>
          </div>
          <div class="grow flex flex-row-reverse">
            <Button
              :loading="this.$resources.course.setValue.loading"
              appearance="primary"
              @click="save()"
              >Save</Button
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { inject } from 'vue'
import { FeatherIcon, Input } from 'frappe-ui'
import CustomAvatar from '@/components/global/CustomAvatar.vue'
import Autocomplete from '@/components/global/Autocomplete.vue'

export default {
  name: 'CourseInfo',
  props: ['course'],
  components: {
    FeatherIcon,
    Input,
    CustomAvatar,
    Autocomplete,
  },
  setup() {
    const user = inject('user')

    return {
      user,
    }
  },
  computed: {
    courseDoc() {
      return this.$resources.course.doc || null
    },
    values() {
      if (this.$resources.course.setValue.loading) {
        return this.values || null
      }
      return {
        description: this.courseDoc ? this.courseDoc.description : null,
      }
    },
  },

  resources: {
    course() {
      return {
        type: 'document',
        doctype: 'Course',
        name: this.course,
        setValue: {
          onSuccess: () => {
            this.$toast({
              title: 'Course Updated.',
              customIcon: 'circle-check',
              appearance: 'success',
            })
          },
        },
      }
    },
  },
  methods: {
    save() {
      this.$resources.course.setValue.submit({
        description: this.values.description,
      })
    },
    cancel() {
      this.$router.push({ name: 'Courses' })
    },
  },
}
</script>

<style></style>
