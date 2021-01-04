<template>
  <div class="chart_box">
    <div>
      <VueApexCharts
        width="100%"
        :height="'540px'"
        :type="type"
        :options="options"
        :series="series"
      ></VueApexCharts>
    </div>
  </div>
</template>

<script>
import VueApexCharts from 'vue-apexcharts'

export default {
  name: 'VueChart',
  components: {
    VueApexCharts
  },
  props: {
    seriesData: Array,
    dataHistory: Array,
    id: String,
    type: String,
    colors: Array
  },
  data: () => {
    return {
      showLabel: false,
      range: 0
    }
  },
  methods: {
    updateRange (range, showLabel) {
      this.range = range
      this.showLabel = showLabel
    }
  },
  computed: {
    stroke () {
      return this.type === 'line' || this.type === 'area'
    },
    series () {
      // 缩放图表
      return this.seriesData.map((d) => {
        d.realData = d.realData ? d.realData : d.data
        d.data = d.realData.slice(this.range)
        return d
      })
    },
    options () {
      return {
        chart: {
          id: this.id,
          type: this.type ? this.type : 'line',
          zoom: {
            enabled: window.innerWidth > 800
          },
          animations: {
            enabled: false
          },
          toolbar: {
            show: true
          }
        },
        colors: this.colors ? this.colors : ['#ff0000', '#3d0707'],
        dataLabels: {
          enabled: this.showLabel,
          textAnchor: 'middle',
          dropShadow: {
            enabled: true
          },
          style: {
            fontSize: '12px'
          }
        },
        stroke: this.stroke ? {
          width: 4
        } : {},
        grid: {
          show: true,
          row: {
            colors: ['#f3f3f3', 'transparent'],
            opacity: 0.5
          }
        },
        xaxis: {
          type: 'datetime',
          categories: this.dataHistory
            .map((d) => {
              return d.date
            })
            .slice(this.range),
          labels: {
            show: true,
            format: 'MM/dd',
            rotate: 0
          },
          lines: {
            show: true
          },
          axisBorder: {
            show: true
          },
          axisTicks: {
            show: true
          }
        },
        yaxis: {
          lines: {
            show: true
          },
          labels: {
            show: true
          }
        }
      }
    }
  }
}
</script>

<style scoped></style>
