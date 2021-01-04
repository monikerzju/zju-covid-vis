<template>
  <div>
    <div v-if="this.chartData">
      <VueChart
        id="line"
        type="area"
        :dataHistory="chartData"
        :seriesData="calcPairs"
        :colors="['#df3838' ,'#0e9100', '#1a1f24']"
      ></VueChart>
    </div>
  </div>
</template>

<script>
import VueChart from '../common/chart.vue'

export default {
  name: 'LineChartOpt',
  props: ['chartData'],
  components: {
    VueChart
  },
  data: () => {
    return {
      showList: [true, true, true],
      optionList: ['确诊', '治愈', '死亡']
    }
  },
  methods: {},
  computed: {
    calcPairs: function () {
      let that = this
      return [
        {
          name: this.optionList[0],
          data: this.chartData.map((d) => {
            return that.showList[0] ? d.total_confirm : 0
          })
        },
        {
          name: this.optionList[1],
          data: this.chartData.map((d) => {
            return that.showList[1] ? d.total_cure : 0
          })
        },
        {
          name: this.optionList[2],
          data: this.chartData.map((d) => {
            return that.showList[2] ? d.total_death : 0
          })
        }
      ]
    }
  },
  watch: {}
}
</script>

<style scoped></style>
