<template>
  <div id="app">
    <!-- Header -->
    <div class="covid_header">
      <div class="header_title">
        <h2>新冠疫情可视化系统</h2>
      </div>
    </div>
    <div class="single_show">
      <div class="section_header">
        <h3>疫情状况显示</h3>
      </div>
      <div>
        <vSelect
          class="select"
          :clearable="false"
          :value="currentCountry"
          :options="countryList"
          @input="switchCountry"
        ></vSelect>
      </div>
      <!-- Bar Chart -->
      <div class="bar_chart">
        <BarChartOpt :chartData="currentCountryData" :currentCountry="currentCountry"></BarChartOpt>
      </div>
      <!-- Line Chart -->
      <div class="line_chart">
        <LineChartOpt :chartData="currentCountryData" :currentCountry="currentCountry"></LineChartOpt>
      </div>
    </div>
    <div class="multi_show">
      <div class="section_header">
        <h3>疫情状况比较</h3>
      </div>
      <!-- World Map -->
      <div class="world_map">
        <WorldMapOpt :chartData= 'mapShowData' :geoData="mapGeoData"></WorldMapOpt>
      </div>
    </div>
  </div>
</template>

<script>
import {countryListReader} from './utils/more.js'
import vSelect from 'vue-select'
import BarChartOpt from './components/bar/opt.vue'
import LineChartOpt from './components/line/opt.vue'
import WorldMapOpt from './components/map/opt.vue'
import globalData from './assets/json/global_data.json'
import perCountryData from './assets/json/countries_data.json'
import mapDrawGeoData from './assets/json/worldCountryGeo_data.json'

export default {
  name: 'App',
  components: {
    vSelect,
    BarChartOpt,
    LineChartOpt,
    WorldMapOpt
  },
  data: () => {
    return {
      currentCountry: null,
      isWorld: null,
      countryList: [],
      display: {},
      currentCountryData: null,
      barChartTitle: null,
      lineChartTitle: null,
      mapShowData: perCountryData,
      mapGeoData: mapDrawGeoData
    }
  },
  async mounted () {
    this.isWorld = true
    this.currentCountry = '全球'
    this.countryList = countryListReader()
    this.currentCountryData = globalData
    this.mapGeoData = mapDrawGeoData
  },
  methods: {
    async switchCountry (country) {
      console.time('switchCountry')
      this.oldCountry = this.currentCountry
      this.currentCountry = country
      if (this.currentCountry === '全球') {
        this.isWorld = true
        this.currentCountryData = globalData
      } else {
        this.isWorld = false
        let i = 0
        for (i = 0; i < perCountryData.length; i = i + 1) {
          if (perCountryData[i].country === this.currentCountry) {
            this.currentCountryData = perCountryData[i].list
            break
          }
        }
      }
      console.timeEnd('switchCountry')
    }
  },
  computed: {}
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
