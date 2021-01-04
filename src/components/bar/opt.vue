<template>
  <div>
    <div class="title">{{chartTitle}}</div>
    <div>
      <vSelect
        class="select"
        :clearable="false"
        :value="whatToShow"
        :options="optionList"
        @input="switchWhatToShow"
      ></vSelect>
    </div>
    <div v-if="this.chartData">
      <VueChart
        id="bar"
        type="bar"
        :dataHistory="chartData"
        :seriesData="calcPairs"
        :colors="barColors"
      ></VueChart>
    </div>
  </div>
</template>

<script>
import VueChart from '../common/chart.vue'
import vSelect from 'vue-select'

export default {
  name: 'BarChartOpt',
  props: ['chartData', 'currentCountry'],
  components: {
    VueChart,
    vSelect
  },
  data: () => {
    return {
      whatToShow: '确诊',
      optionList: ['确诊', '治愈', '死亡', '新增确诊', '新增治愈', '新增死亡', '治愈率', '死亡率'],
      barColors: ['#df3838'],
      halfChartTitle: '新冠疫情确诊情况',
      lastWhatToShow: '确诊',
      chartTitle: null
    }
  },
  methods: {
    async switchWhatToShow (opt) {
      console.time('switchWhatToShow')
      this.lastWhatToShow = this.whatToShow
      this.whatToShow = opt
      if (this.whatToShow === '确诊' || this.whatToShow === '新增确诊') {
        this.barColors = ['#df3838']
      } else if (this.whatToShow === '治愈' || this.whatToShow === '新增治愈' || this.whatToShow === '治愈率') {
        this.barColors = ['#0e9100']
      } else {
        this.barColors = ['#1a1f24']
      }
      console.timeEnd('switchWhatToShow')
    }
  },
  computed: {
    calcPairs: function () {
      let that = this
      that.halfChartTitle = that.halfChartTitle.replace(that.lastWhatToShow, that.whatToShow)
      that.chartTitle = that.currentCountry + that.halfChartTitle
      return [
        {
          name: this.whatToShow,
          data: this.chartData.map((d) => {
            if (that.whatToShow === '死亡') {
              return d.total_death
            }
            if (that.whatToShow === '治愈') {
              return d.total_cure
            }
            if (that.whatToShow === '确诊') {
              return d.total_confirm
            }
            if (that.whatToShow === '新增死亡') {
              return d.daily_death
            }
            if (that.whatToShow === '新增治愈') {
              return d.daily_cure
            }
            if (that.whatToShow === '新增确诊') {
              return d.daily_confirm
            }
            if (that.whatToShow === '治愈率') {
              return d.cure_rate
            }
            if (that.whatToShow === '死亡率') {
              return d.death_rate
            }
          })
        }
      ]
    }
  },
  watch: {}
}
</script>

<style scoped></style>
