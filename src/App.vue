np<template>
  <section class=" bg-img pt-100 pb-70">
    <div class="container">
      <div class="section-title">
        <span>our presentation</span>
        <h2>疫情信息可视化显示</h2>
        <p>
          这是浙江大学信息可视化课程的期末作业。在本次作业中，我们选择了D3和VueApexChart去描述全世界范围和每个国家在2020年2月以来的COVID-19疫情变化。
        </p>
      </div>
      <div class="row">
        <div class="single-services-box col-lg-4 col-sm-6">
          <img src="./pic/icon0.png" width="100" height="100" />
          <h3>国家疫情查看</h3>
          <p>
            具体疫情信息查询，可以从全球整体或各个国家了解新冠肺炎疫情的状况，同时提供全球疫情状况的折线图查看
          </p>
          <p class="read-more" v-on:click="dischart=1"> Read Details </p>
        </div>
        <div class="single-services-box col-lg-4 col-sm-6">
          <img src="./pic/icon1.png" width="100" height="100" />
          <h3>疫情状况比较</h3>
          <p>
            各国家新冠疫情确诊人数的柱状图，显示了统计数据以来的top10进行动态显示，对疫情变化有清晰的查看
          </p>
          <p class="read-more" v-on:click="dischart=2"> Read Details </p>
        </div>
        <div class="single-services-box col-lg-4 col-sm-6">
          <img src="./pic/icon2.png" width="100" height="100" />
          <h3>世界疫情地图</h3>
          <p>
            用着色地图的方式对新冠疫情各种数据进行显示，可以修改日期和数据类别，单项数据更加直观且具有整体性
          </p>
          <p class="read-more" v-on:click="dischart=3"> Read Details </p>
        </div>
      </div>
    </div>
    <div id="app">
    <div class="single_show" v-if="dischart==1">
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
    <div class="multi_show"  v-if="dischart==2">
      <div class="section_header">
        <h3>疫情状况比较</h3>
      </div>
      <!-- Compare Animation -->
      <div class="cabar_chart">
        <CompareAnimation :cabarDataOri="cabarDataOri"></CompareAnimation>
      </div>
    </div>
    <div class="map_show" v-if="dischart==3">
      <!-- World Map -->
      <div class="map_title" >
        <h3>世界疫情地图</h3>
      </div>
      <div class="world_map">
        <WorldMapOpt :chartData= 'mapShowData' :geoData="mapGeoData"></WorldMapOpt>
      </div>
    </div>
    <div v-if="dischart!=0">
      <p class="read-more" v-on:click="dischart=0"> 返回 </p>
    </div>
  </div>
  </section>
</template>
<script>
import { countryListReader } from './utils/more.js'
import vSelect from 'vue-select'
import BarChartOpt from './components/bar/opt.vue'
import LineChartOpt from './components/line/opt.vue'
import WorldMapOpt from './components/map/opt.vue'
import globalData from './assets/json/global_data.json'
import perCountryData from './assets/json/countries_data.json'
import mapDrawGeoData from './assets/json/worldCountryGeo_data.json'
import CompareAnimation from './components/comparison/cabar.vue'
import cabarData from './assets/json/cabarData.json'
/* import country from './country' */
import router from './router/index'
export default {
  name: 'App',
  components: {
    vSelect,
    BarChartOpt,
    LineChartOpt,
    WorldMapOpt,
    CompareAnimation
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
      mapGeoData: mapDrawGeoData,
      cabarDataOri: cabarData,
      dischart: 0
    }
  },
  async mounted () {
    this.isWorld = true
    this.currentCountry = '全球'
    this.countryList = countryListReader()
    this.currentCountryData = globalData
    this.mapGeoData = mapDrawGeoData
    this.cabarDataOri = cabarData
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
    },
    gocountry () {
      router.push('/country')
    }
  },
  computed: {}
}

</script>
