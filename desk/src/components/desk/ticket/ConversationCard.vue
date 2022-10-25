<template>
	<div class="flex flex-col my-[16px] px-[10px]">
		<div class="flex flex-row justify-between">
			<div class="flex flex-row items-center space-x-[8px]">
				<CustomAvatar :label="userName" :imageURL="profilePicUrl" :imageOwner="emailId" size="sm" />
				<div class="h-full">
					<div
						class="flex flex-col select-none"
					>
						<div
							class="shrink-0 flex flex-row items-center cursor-pointer"
							@click="
								() => {
									showCcBcc = !showCcBcc
								}
							"
						>
							<div class="truncate text-[14px] font-normal max-w-[200px]">{{ userName }}</div>
							<FeatherIcon
								class="h-[15px] w-[15px] stroke-gray-500 ml-[0.125rem]"
								:name="showCcBcc ? 'chevron-up' : 'chevron-down'"
							/>
						</div>
						<div
							v-if="showCcBcc"
							class="overflow-y-scroll"
							:style="{
								height:
									viewportWidth > 768
										? `calc(100vh - ${getOffsetHeight}px)`
										: null,
							}"
							>
							<div class="prose prose-p:my-1 text-[13px] text-gray-700" style="border: 0px;" >cc: {{ cc }}</div>
							<div class="prose prose-p:my-1 text-[13px] text-gray-700" style="border: 0px;" >bcc: {{ bcc }}</div>
						</div>
					</div>
				</div>
			</div>
			<a :title="$dayjs(time)" class="text-gray-500 text-[12px] select-none">{{ $dayjs.longFormating($dayjs(time).fromNow()) }}</a>
		</div>
		<div class="pl-[32px] pt-[6px]">
			<div class="flex flex-col">
				<div class="prose prose-p:my-1 text-[13px] text-gray-700" style="border: 0px;" v-html="cleanedMessage"></div>
				<div v-if="attachments.length > 0" class="flex flex-wrap text-base mt-[8px]">
					<div v-for="attachment in attachments" :key="attachment">
						<a :href="attachment.file_url" target="_blank" class="py-[4px] max-w-[180px] rounded-[6px] border px-[8px] text-gray-700 font-normal text-[12px] hover:underline flex items-center space-x-[8px] border-gray-200 mr-[10px] mb-[5px]">
							<FeatherIcon name="paperclip" class="h-[12px] w-[12px] shrink-0" />
							<span class="truncate">{{ attachment.file_name }}</span>
						</a>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { FeatherIcon } from 'frappe-ui'
import CustomAvatar from '@/components/global/CustomAvatar.vue'
import { remove_script_and_style } from '@/utils'
import { ref } from 'vue'

export default {
	name: 'ConversationCard',
	props: ['userName', 'emailId', 'profilePicUrl', 'time', 'message', 'color', 'attachments', 'cc', 'bcc'],
	components: {
		FeatherIcon,
		CustomAvatar
	},
	computed: {
		cleanedMessage() {
			if (this.message) {
				return remove_script_and_style(this.message)
			}
			return ''
		}
	},
	setup() {
		const showCcBcc = ref(false)

		return {showCcBcc}
	}
}
</script>

<style>

</style>