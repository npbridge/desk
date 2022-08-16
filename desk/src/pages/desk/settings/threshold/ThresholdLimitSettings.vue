<template>
  <div class="p-5 overflow-auto h-full">
    <div class="mb-[16px]">
      <div class="font-normal">Additional Settings</div>
    </div>
    <div class="w-53 flex flex-row space-x-2 mb-[30px]">
      <Input
        label="Threshold Limit"
        type="number"
        v-model="thresholdLimit"
        class="text-gray-600 w-52"
        @input="checkLimitChange"
      />
      <div class="mt-[22px]">
        <Button
          :disabled="!thresholdLimitChanged"
          appearance="primary"
          @click="updateLimitChange"
        >
          Save
        </Button>
      </div>
    </div>
    <div class="w-53 flex flex-row space-x-2 mb-[30px]">
      <Input
        label="Use Bot Answers"
        class="text-gray-600"
        type="checkbox"
        @click="checkUseBotAnswers"
        :checked="useBotAnswers"
      />
      <div>
        <Button
          :disabled="!useBotAnswersChanged"
          appearance="primary"
          @click="updateUseBotAnswers"
        >
          Save
        </Button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from '@vue/reactivity'
import { Input, debounce } from 'frappe-ui'

export default {
  name: 'ThresholdLimitSettings',
  components: {
    Input,
  },
  setup() {
    const thresholdLimit = ref('')
    const newThresholdLimit = ref('')
    const thresholdLimitChanged = ref(false)
    const useBotAnswers = ref('')
    const newUseBotAnswers = ref('')
    const useBotAnswersChanged = ref(false)

    return {
      thresholdLimit,
      newThresholdLimit,
      thresholdLimitChanged,
      useBotAnswers,
      newUseBotAnswers,
      useBotAnswersChanged,
    }
  },
  resources: {
    thresholdLimit() {
      return {
        method: 'frappedesk.api.website.threshold_limit',
        auto: true,
        onSuccess: (res) => {
          this.thresholdLimit = res
        },
      }
    },
    useBotAnswers() {
      return {
        method: 'frappedesk.api.website.use_bot_answers',
        auto: true,
        onSuccess: (res) => {
          this.useBotAnswers = res
          this.newUseBotAnswers = res
        },
      }
    },
    updateLimitChange() {
      return {
        method: 'frappedesk.api.settings.update_threshold_limit_change',
        onSuccess: (res) => {
          this.thresholdLimit = res
          this.$toast({
            title: 'Threshold limit updated!!',
            customIcon: 'circle-check',
            appearance: 'success',
          })
          this.thresholdLimitChanged = false
        },
        onError: (err) => {
          console.log(err)
          this.$toast({
            title: 'Error updating threshold limit',
            text: err,
            customIcon: 'circle-x',
            appearance: 'error',
          })
        },
      }
    },
    updateUseBotAnswers() {
      return {
        method: 'frappedesk.api.settings.update_use_bot_answers',
        onSuccess: (res) => {
          this.useBotAnswers = res
          this.$toast({
            title: 'Use Bot Answers Flag Updated!!',
            customIcon: 'circle-check',
            appearance: 'success',
          })
          this.useBotAnswersChanged = false
        },
        onError: (err) => {
          console.log(err)
          this.$toast({
            title: 'Error updating Use Bot Answers Flag',
            text: err,
            customIcon: 'circle-x',
            appearance: 'error',
          })
        },
      }
    },
  },
  methods: {
    checkLimitChange: debounce(function (limit) {
      this.thresholdLimitChanged = this.thresholdLimit != limit
      this.newThresholdLimit = parseFloat(limit)
    }, 500),
    checkUseBotAnswers: debounce(function () {
      this.newUseBotAnswers = !this.newUseBotAnswers
      this.useBotAnswersChanged = this.useBotAnswers != this.newUseBotAnswers
    }, 500),
    updateLimitChange() {
      this.$resources.updateLimitChange.submit({
        limit: this.newThresholdLimit,
      })
    },
    updateUseBotAnswers() {
      if (this.newUseBotAnswers == true)
        this.$resources.updateUseBotAnswers.submit({
          flag: 1,
        })
      else
        this.$resources.updateUseBotAnswers.submit({
          flag: 0,
        })
    },
  },
  mounted() {
    this.$event.emit('set-selected-setting', 'Additional Settings')
  },
}
</script>
