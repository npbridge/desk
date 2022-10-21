<template>
  <div class="flex flex-col">
    <div class="flex border-b h-[100px] px-[24px] shrink-0 mt-[15px] mb-[5px]">
      <div>
        <div class="grow my-auto text-[17px] font-semibold text-gray-900">
          Comparison Reports
        </div>
        <hr />
        <p class="grow my-auto text-[13px] text-black-600 mt-[10px] mb-[10px]">
          Welcome! This is the "Comparison Reports" section where you can select
          any of the reports listed below for which you'd want to compare data.
          You can specify the date ranges you want to compare in the format of
          DD-MM-YYYY by clicking on the report of your choosing.
        </p>
      </div>
    </div>
    <div
      class="bg-[#F7F7F7] group flex items-center text-base font-medium text-gray-500 py-[10px] pl-[11px] pr-[17px] rounded-[6px]"
    >
      <div class="flex flex-row items-center group w-full">
        <div class="sm:w-4/12">Name</div>
        <div class="sm:w-7/12">Details</div>
        <div class="sm:w-3/12 pl-[0.5rem]">Link</div>
      </div>
    </div>
    <div
      id="rows"
      class="flex flex-col space-y-2 overflow-scroll"
      :style="{
        height: viewportWidth > 768 ? 'calc(100vh - 6.4rem)' : null,
      }"
    >
      <div v-for="report in reports" :key="report.heading">
        <div class="block rounded-[6px] py-[7px] px-[11px]">
          <div class="flex items-center text-base">
            <div class="sm:w-4/12 pr-10">
              {{ report.heading }}
            </div>
            <div class="sm:w-7/12 pr-10">
              {{ report.information }}
            </div>
            <div class="sm:w-3/12 pr-10">
              <Button
                @click="
                  () => {
                    $router.push(report.to)
                  }
                "
                >View</Button
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'Reports',
  setup() {
    const reports = ref()
    return {
      reports,
    }
  },
  mounted() {
    this.reports = [
      {
        heading: 'Tickets Received Over Time',
        information:
          'Find and compare the number of tickets received over time',
        to: {
          path: '/app/query-report/Tickets Received Over Time',
        },
      },
      {
        heading: 'Tickets Replied Over Time',
        information:
          'Find and compare the number of tickets replied over time',
        to: {
          path: '/app/query-report/Tickets Replied To Over Time',
        },
      },
      {
        heading: 'Tickets Resolved Over Time',
        information:
          'Find and compare the number of tickets resolved over time',
        to: {
          path: '/app/query-report/Tickets Resolved Over Time',
        },
      },
      {
        heading: 'Tickets Closed Over Time',
        information: 'Find and compare the number of closed tickets over time',
        to: {
          path: '/app/query-report/Tickets Closed Over Time',
        },
      },
       {
         heading: 'Tickets Unresolved Over Time',
         information:
           'Find and compare the number of unresolved tickets over time',
         to: {
           path: '/app/query-report/Tickets Un-Resolved Over Time',
         },
       },
    ]
  },
}
</script>
