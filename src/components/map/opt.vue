<template>
  <div>
    <div>
      <vSelect
        class='select'
        :clearable='false'
        :value='whatToShow'
        :options='optionList'
        @input='switchWhatToShow'
      ></vSelect>
    </div>
    <div>
      <vSelect
        class='select'
        :clearable='false'
        :value='yearWhatToShow'
        :options='yearOptionList'
        @input='switchYear'
      ></vSelect>
    </div>
    <div>
      <vSelect
        class='select'
        :clearable='false'
        :value='monthWhatToShow'
        :options='monthOptionList'
        @input='switchMonth'
      ></vSelect>
    </div>
    <div>
      <vSelect
        class='select'
        :clearable='false'
        :value='dayWhatToShow'
        :options='dayOptionList'
        @input='switchDay'
      ></vSelect>
    </div>
    <div id="map-container" :style="{width:'document.body.clientWidth',height:'1080px'}" >
      <meta name='viewport' content='width=device-width initial-scale=1.0' />
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'
import vSelect from 'vue-select'

export default {
  name: 'WorldMapOpt',
  props: ['chartData', 'geoData'],
  components: {
    vSelect
  },
  data () {
    return {
      g: null,
      title: null,
      svg: null,
      worldBase: null,
      legend: null,
      color: d3.scaleOrdinal(d3.schemeReds[6]).domain(['0-1k人', '1k-1w人', '1w-10w人', '10w-100w人', '100w-1000w人', '1000w人及以上']),
      level: ['0-1k人', '1k-1w人', '1w-10w人', '10w-100w人', '100w-1000w人', '1000w人及以上'],
      countLevel: [1000, 10000, 100000, 1000000, 10000000],
      whatToShow: '确诊',
      lastWhatToShow: '确诊',
      optionList: ['确诊', '治愈', '死亡', '新增确诊', '新增治愈', '新增死亡', '治愈率', '死亡率'],
      yearWhatToShow: '2020年',
      yearLastWhatToShow: '2020年',
      yearOptionList: ['2020年', '2021年'],
      monthWhatToShow: '12月',
      monthLastWhatToShow: '12月',
      monthOptionList: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
      dayWhatToShow: '31日',
      dayLastWhatToShow: '31日',
      dayOptionList: ['1日', '2日', '3日', '4日', '5日', '6日', '7日', '8日', '9日', '10日', '11日', '12日', '13日', '14日', '15日', '16日', '17日', '18日', '19日', '20日', '21日', '22日', '23日', '24日', '25日', '26日', '27日', '28日', '29日', '30日', '31日'],
      year: '2020',
      month: '12',
      day: '31',
      width: 1250,
      height: 900,
      date: '2020-12-31',
      dataType: ['total_confirm', 'daily_confirm', 'total_death', 'daily_death', 'total_cure', 'daily_cure', 'cure_rate', 'death_rate'],
      typeNow: 'total_confirm'
    }
  },

  mounted () {
    this.initMap()
    this.drawMap()
  },

  methods: {
    async switchWhatToShow (opt) {
      this.lastWhatToShow = this.whatToShow
      this.whatToShow = opt
      if (this.whatToShow === '确诊') {
        this.typeNow = this.dataType[0]
        this.level = ['0-1k人', '1k-1w人', '1w-10w人', '10w-100w人', '100w-1000w人', '1000w人及以上']
        this.countLevel = [1000, 10000, 100000, 1000000, 10000000]
        this.color = d3.scaleOrdinal(d3.schemeReds[6]).domain(this.level)
        this.reDraw()
      } else if (this.whatToShow === '新增确诊') {
        this.typeNow = this.dataType[1]
        this.level = ['0-100人', '100-1k人', '1k-1w人', '1w-10w人', '10w-100w人', '100w人及以上']
        this.countLevel = [100, 1000, 10000, 100000, 1000000]
        this.color = d3.scaleOrdinal(d3.schemeReds[6]).domain(this.level)
        this.reDraw()
      } else if (this.whatToShow === '治愈') {
        this.typeNow = this.dataType[4]
        this.level = ['0-1k人', '1k-1w人', '1w-10w人', '10w-100w人', '100w-300w人', '300w人及以上']
        this.countLevel = [1000, 10000, 100000, 1000000, 3000000]
        this.color = d3.scaleOrdinal(d3.schemeGreens[6]).domain(this.level)
        this.reDraw()
      } else if (this.whatToShow === '新增治愈') {
        this.typeNow = this.dataType[5]
        this.level = ['0-100人', '100-1k人', '1k-1w人', '1w-5w人', '5w-10w人', '10w人及以上']
        this.countLevel = [100, 1000, 10000, 50000, 100000]
        this.color = d3.scaleOrdinal(d3.schemeGreens[6]).domain(this.level)
        this.reDraw()
      } else if (this.whatToShow === '治愈率') {
        this.typeNow = this.dataType[6]
        this.level = ['0%-20%', '20%-35%', '35%-50%', '50%-65%', '65%-85%', '85%-100%']
        this.countLevel = [0.2, 0.35, 0.5, 0.650, 0.85]
        this.color = d3.scaleOrdinal(d3.schemeGreens[6]).domain(this.level)
        this.reDraw()
      } else if (this.whatToShow === '死亡') {
        this.typeNow = this.dataType[2]
        this.level = ['0-1k人', '1k-1w人', '1w-10w人', '10w-100w人', '100w-1000w人', '1000w人及以上']
        this.countLevel = [1000, 10000, 100000, 1000000, 10000000]
        this.color = d3.scaleOrdinal(d3.schemeGreys[6]).domain(this.level)
        this.reDraw()
      } else if (this.whatToShow === '新增死亡') {
        this.typeNow = this.dataType[3]
        this.level = ['0-10人', '10-100人', '100-1k人', '1w-5k人', '5k-1w人', '1w人及以上']
        this.countLevel = [10, 100, 1000, 5000, 10000]
        this.color = d3.scaleOrdinal(d3.schemeGreys[6]).domain(this.level)
        this.reDraw()
      } else if (this.whatToShow === '死亡率') {
        this.typeNow = this.dataType[7]
        this.level = ['0%-1%', '1%-5%', '5%-10%', '10%-15%', '15%-20%', '20%及以上']
        this.countLevel = [0.01, 0.05, 0.1, 0.15, 0.2]
        this.color = d3.scaleOrdinal(d3.schemeGreys[6]).domain(this.level)
        this.reDraw()
      }
    },

    async switchYear (opt) {
      this.yearLastWhatToShow = this.yearWhatToShow
      this.yearWhatToShow = opt
      this.year = this.yearWhatToShow.substr(0, 4)
      this.date = this.year + '-' + this.month + '-' + this.day
      this.worldBaseInit()
    },
    async switchMonth (opt) {
      this.monthLastWhatToShow = this.monthWhatToShow
      this.monthWhatToShow = opt
      if (this.monthWhatToShow.length === 2) {
        this.month = '0' + this.monthWhatToShow.substr(0, 1)
      } else {
        this.month = this.monthWhatToShow.substr(0, 2)
      }
      this.date = this.year + '-' + this.month + '-' + this.day
      this.worldBaseInit()
    },
    async switchDay (opt) {
      this.dayLastWhatToShow = this.dayWhatToShow
      this.dayWhatToShow = opt
      if (this.dayWhatToShow.length === 2) {
        this.day = '0' + this.dayWhatToShow.substr(0, 1)
      } else {
        this.day = this.dayWhatToShow.substr(0, 2)
      }
      this.date = this.year + '-' + this.month + '-' + this.day
      this.worldBaseInit()
    },
    initMap () {
      // 指定图表的宽高
      this.width = document.body.clientWidth
      this.height = 800

      d3.select('#map-container')
        .style('width', 'device-width')
        .style('height', '1000px')

      // 添加svg
      this.svg = d3.select('#map-container').append('svg')
        .attr('width', '100%')
        .attr('height', '1000px')

      // 添加g标签
      this.g = this.svg.append('g')
        .attr('class', 'chart')
    },

    drawMap () {
      // 去掉南极洲
      const worldGeoFeatures = this.geoData.features.filter(d => d.properties.name !== 'Antarctica')
      // 去掉南极洲以后的世界json数据
      const worldNoATAGeo = {
        type: 'FeatureCollection',
        features: worldGeoFeatures
      }

      // 地图投影-墨卡托投影
      const projection = d3.geoMercator().fitExtent([
        [0, 100],
        [this.width, this.height]
      ], worldNoATAGeo)

      // 地理路径生成器
      const path = d3.geoPath(projection)

      // 绘制世界地图
      this.worldBase = this.g.append('g')
        .attr('class', 'worldMap')
        .selectAll('path')
        .data(worldGeoFeatures)
        .join('path')
        .attr('d', d => path(d))
        .attr('fill', '#BBB')
        .attr('stroke', 'white')
      this.worldBaseInit()
      this.legendInit()
    },

    worldBaseInit () {
      this.worldBase.style('fill', d => {
        const countryName = d.properties.name
        // 某一个国家的所有数据
        const OneCountryData = this.chartData.filter(d => d.country === countryName)
        // 某一个国家某一天的数据
        let count = 0
        if (OneCountryData.length > 0) {
          OneCountryData[0].list.map(d => {
            if (d.date === this.date) {
              if (this.typeNow === 'total_confirm') {
                count = d.total_confirm
              } else if (this.typeNow === 'daily_confirm') {
                count = d.daily_confirm
              } else if (this.typeNow === 'total_death') {
                count = d.total_death
              } else if (this.typeNow === 'daily_death') {
                count = d.daily_death
              } else if (this.typeNow === 'total_cure') {
                count = d.total_cure
              } else if (this.typeNow === 'daily_cure') {
                count = d.daily_cure
              } else if (this.typeNow === 'cure_rate') {
                count = d.cure_rate
              } else if (this.typeNow === 'death_rate') {
                count = d.death_rate
              }
            }
          })
        }
        const levelIndex = count < this.countLevel[0] ? 0 : count < this.countLevel[1] ? 1 : count < this.countLevel[2] ? 2 : count < this.countLevel[3] ? 3 : count < this.countLevel[4] ? 4 : 5
        return this.color(this.level[levelIndex])
      })
    },

    legendInit () {
      this.legend = this.g.append('g')
        .attr('class', 'legend')
      this.legend.selectAll('rect')
        .data(this.level)
        .join('rect')
        .attr('width', 30)
        .attr('height', 15)
        .attr('x', this.width * 0.15)
        .attr('y', (d, i) => (this.height * 0.65) + (i + 1) * 40)
        .style('fill', d => this.color(d))

      this.legend.selectAll('text')
        .data(this.level)
        .join('text')
        .attr('x', this.width * 0.15 + 35)
        .attr('y', (d, i) => (this.height * 0.65 + 15) + (i + 1) * 40)
        .text(d => d)
        .attr('text-anchor', 'start')
        .attr('font-size', '15')
    },

    legendChange () {
      this.legend.selectAll('rect')
        .style('fill', d => this.color(d))
      this.legend.selectAll('text')
        .data(this.level)
        .join('text')
        .text(d => d)
    },

    reDraw () {
      this.worldBaseInit()
      this.legendChange()
    }
  }
}

</script>

<style></style>
