<template>
  <Button @click="openSidebar" class="md:hidden">
    <CustomIcons name="justify" width="20" height="20" class="" />
  </Button>
</template>

<script>
import CustomIcons from '@/components/desk/global/CustomIcons.vue'

export default {
  name: 'SidebarCollapser',
  components: {
    CustomIcons,
  },
  methods: {
    openSidebar() {
      // document.getElementById('main').style.marginLeft = '241px'
      document.getElementById('sidebar').style.width = '100%'
      document.getElementById('sidebar').style.visibility = 'visible'
    },
  },
}
</script>
