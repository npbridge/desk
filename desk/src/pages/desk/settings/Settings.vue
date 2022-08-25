<template>
	<div v-if="initialized">
		<SettingsTopPanel />
		<div :style="{ height: viewportWidth > 768 ? 'calc(100vh - 55px)' : null }" class="flex">
			<div class="w-[167px] border-r">
				<SettingsSideBarMenu />
			</div>
			<div class="grow h-full">
				<router-view v-slot="{ Component }">
					<component :is="Component" />
				</router-view>
			</div>
		</div>
	</div>
</template>

<script>
import SettingsSideBarMenu from "@/components/desk/settings/SettingsSideBarMenu.vue"
import SettingsTopPanel from "@/components/desk/settings/SettingsTopPanel.vue"

import { inject } from 'vue'

export default {
	name: 'Settings',
	components: {
		SettingsSideBarMenu,
		SettingsTopPanel
	},
	setup() {
		const viewportWidth = inject('viewportWidth')
		const user = inject('user')

		return { 
			viewportWidth ,
			user
		}
	},
	computed: {
		initialized() {
			const foundRoleInfo = this.user.doc.roles.find(role => role.role === 'Helpdesk Agent')
			if (foundRoleInfo) return false
			return true
		}
	},
}
</script>

<style>

</style>