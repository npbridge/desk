<template>
  <div class="min-w-[304px] px-[24px] py-[10px]">
    <div class="form w-full flex flex-col">
      <div class="flex flex-col space-y-[24px]">
        <Input
          class="grow"
          label="Tag Name"
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
              :loading="this.$resources.tag.setValue.loading"
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
  name: 'TagInfo',
  props: ['tag'],
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
    tagDoc() {
      return this.$resources.tag.doc || null
    },
    values() {
      if (this.$resources.tag.setValue.loading) {
        return this.values || null
      }
      return {
        description: this.tagDoc ? this.tagDoc.description : null,
      }
    },
  },

  resources: {
    tag() {
      return {
        type: 'document',
        doctype: 'Helpdesk Tag',
        name: this.tag,
        setValue: {
          onSuccess: () => {
            this.$toast({
              title: 'Tag Updated.',
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
      this.$resources.tag.setValue.submit({
        description: this.values.description,
      })
    },
    cancel() {
      this.$router.push({ name: 'Tags' })
    },
  },
}
</script>

<style></style>
