<template>
  <div>
    <div class="title">{{chartTitle}}</div>
    <div>
      <vSelect
        class="select"
        :clearable="false"
        :value="metaShow"
        :options="metaOptionList"
        @input="switchMetaShow"
      ></vSelect>
    </div>
    <div v-if="this.chartData && this.metaShow === '人数'">
      <div>
        <VueChart
          v-if="selectedOptions.length > 0"
          id="line"
          type="area"
          :dataHistory="chartData"
          :seriesData="series"
          :colors="threeColors"
        ></VueChart>
      </div>
      <div>
        <vSelect
          multiple
          placeholder="请选择想要显示的数据"
          label="options"
          v-model="selectedOptions"
          :options="trueOptions"
          :selectable="() => true"
        />
      </div>
    </div>
    <div v-else-if="this.chartData">
      <div>
        <VueChart
          v-if="rateSelectedOptions.length > 0"
          id="rate_line"
          type="area"
          :dataHistory="chartData"
          :seriesData="series"
          :colors="twoColors"
        ></VueChart>
      </div>
      <div>
        <vSelect
          multiple
          placeholder="请选择想要显示的数据"
          label="options"
          v-model="rateSelectedOptions"
          :options="trueRateOptions"
          :selectable="() => true"
        />
      </div>
    </div>
  </div>
</template>

<script>
import VueChart from '../common/chart.vue'
import vSelect from 'vue-select'

export default {
  name: 'LineChartOpt',
  props: ['chartData', 'currentCountry'],
  components: {
    VueChart,
    vSelect
  },
  data: () => {
    return {
      metaShow: '人数',
      metaOptionList: ['人数', '概率'],
      optionList: ['确诊', '治愈', '死亡'],
      colorList: ['#df3838', '#0e9100', '#1a1f24'],
      rateOptionList: ['治愈率', '死亡率'],
      chartTitle: '全球新冠疫情变化情况',
      selectedOptions: ['确诊', '治愈', '死亡'],
      rateSelectedOptions: ['治愈率', '死亡率'],
      threeColors: ['#df3838', '#0e9100', '#1a1f24'],
      twoColors: ['#df3838', '#0e9100', '#1a1f24'],
      series: [],
      trueOptions: [],
      trueRateOptions: []
    }
  },
  methods: {
    async switchMetaShow (opt) {
      console.time('switchMetaShow')
      this.metaShow = opt
      console.timeEnd('switchMetaShow')
    },
    isInArray (arr, value) {
      for (var i = 0; i < arr.length; i = i + 1) {
        if (arr[i] === value) {
          return true
        }
      }
      return false
    },
    calcPairs () {
      let that = this
      that.chartTitle = this.currentCountry + '新冠疫情变化情况'
      let iter
      that.trueOptions = []
      that.trueRateOptions = []
      if (this.metaShow === '人数') {
        for (iter = 0; iter < that.optionList.length; iter = iter + 1) {
          if (this.isInArray(that.selectedOptions, that.optionList[iter]) === false) {
            that.trueOptions.push(that.optionList[iter])
          }
        }
        let tempList = []
        let tempShowList = []
        tempShowList.push(that.isInArray(that.selectedOptions, that.optionList[0]))
        tempShowList.push(that.isInArray(that.selectedOptions, that.optionList[1]))
        tempShowList.push(that.isInArray(that.selectedOptions, that.optionList[2]))
        that.threeColors = []
        if (tempShowList[0]) {
          let tempObj = {
            name: this.optionList[0],
            data: this.chartData.map((d) => {
              return d.total_confirm
            })
          }
          tempList.push(tempObj)
          that.threeColors.push(this.colorList[0])
        }
        if (tempShowList[1]) {
          let tempObj = {
            name: this.optionList[1],
            data: this.chartData.map((d) => {
              return d.total_cure
            })
          }
          tempList.push(tempObj)
          that.threeColors.push(this.colorList[1])
        }
        if (tempShowList[2]) {
          let tempObj = {
            name: this.optionList[2],
            data: this.chartData.map((d) => {
              return d.total_death
            })
          }
          tempList.push(tempObj)
          that.threeColors.push(this.colorList[2])
        }
        that.series = tempList
      } else {
        for (iter = 0; iter < that.rateOptionList.length; iter = iter + 1) {
          if (this.isInArray(that.rateSelectedOptions, that.rateOptionList[iter]) === false) {
            that.trueRateOptions.push(that.rateOptionList[iter])
          }
        }
        let tempList = []
        let tempShowList = []
        tempShowList.push(that.isInArray(that.rateSelectedOptions, that.rateOptionList[0]))
        tempShowList.push(that.isInArray(that.rateSelectedOptions, that.rateOptionList[1]))
        that.twoColors = []
        if (tempShowList[0]) {
          let tempObj = {
            name: this.rateOptionList[0],
            data: this.chartData.map((d) => {
              return d.cure_rate
            })
          }
          tempList.push(tempObj)
          that.twoColors.push(this.colorList[1])
        }
        if (tempShowList[1]) {
          let tempObj = {
            name: this.rateOptionList[1],
            data: this.chartData.map((d) => {
              return d.death_rate
            })
          }
          tempList.push(tempObj)
          that.twoColors.push(this.colorList[2])
        }
        that.series = tempList
      }
    }
  },
  computed: {},
  watch: {
    selectedOptions: function () {
      this.calcPairs()
    },
    rateSelectedOptions: function () {
      this.calcPairs()
    },
    chartData: function () {
      this.calcPairs()
    },
    metaShow: function () {
      this.calcPairs()
    }
  }
}
</script>

<style scoped></style>
