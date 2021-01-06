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
      <DateSlider
        :startDate='firstDate'
        :endDate='lastDate'
        :currentDate='date'
        @switchDate='switchDate'
      />
    </div>
    <div id="map-container" :style="{width:'document.body.clientWidth',height:'1080px'}" >
      <meta name='viewport' content='width=device-width initial-scale=1.0' />
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'
import vSelect from 'vue-select'
import DateSlider from '../common/slider.vue'

export default {
  name: 'WorldMapOpt',
  props: ['chartData', 'geoData'],
  components: {
    vSelect,
    DateSlider
  },
  data () {
    return {
      g: null,
      title: null,
      svg: null,
      worldBase: null,
      legend: null,
      tooltip: null,
      color: d3.scaleOrdinal(d3.schemeReds[6]).domain(['0-1k人', '1k-1w人', '1w-10w人', '10w-100w人', '100w-1000w人', '1000w人及以上']),
      level: ['0-1k人', '1k-1w人', '1w-10w人', '10w-100w人', '100w-1000w人', '1000w人及以上'],
      countLevel: [1000, 10000, 100000, 1000000, 10000000],
      whatToShow: '确诊',
      lastWhatToShow: '确诊',
      optionList: ['确诊', '治愈', '死亡', '新增确诊', '新增治愈', '新增死亡', '治愈率', '死亡率'],
      width: 1250,
      height: 900,
      date: '2020-12-31',
      dataType: ['total_confirm', 'daily_confirm', 'total_death', 'daily_death', 'total_cure', 'daily_cure', 'cure_rate', 'death_rate'],
      typeNow: 'total_confirm',
      // For the Slider
      firstDate: '2020-01-22',
      lastDate: '2021-21-31'
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
        this.level = ['0%-1%', '1%-3%', '3%-5%', '5%-10%', '10%-20%', '20%及以上']
        this.countLevel = [0.01, 0.03, 0.05, 0.10, 0.2]
        this.color = d3.scaleOrdinal(d3.schemeGreys[6]).domain(this.level)
        this.reDraw()
      }
    },

    async switchDate (opt) {
      this.date = opt
      this.worldBaseInit()
      this.tooltipInit()
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
      this.tooltipInit()
    },

    worldBaseInit () {
      this.worldBase.style('fill', d => {
        const countryName = d.properties.name
        // 某一个国家的所有数据
        const OneCountryData = this.chartData.filter(d => d.country === countryName)
        if (OneCountryData.length > 0) {
          this.lastDate = OneCountryData[0].list[OneCountryData[0].list.length - 1].date
        }
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

    tooltipInit () {
      // 添加提示框
      this.tooltip = this.g.append('g')
        .attr('class', 'tooltip')
        .attr('opacity', 0)

      this.tooltip.append('rect')
        .attr('fill', 'white')
        .attr('rx', 0)
        .attr('ry', 0)
        .attr('width', 180)
        .attr('height', 40)
        .attr('stroke', 'black')
        .attr('style', 'stroke-width:1')

      this.tooltip.append('text')
        .attr('font-size', 12)
        .attr('transform', `translate(${15},${25})`)

      // 不知道为啥在这里会把this.chartDate\this.data识别为undefined，所以在外面声明一个全局变量缓存数据
      let dataCache = this.chartData
      let dateCache = this.date
      let typeNowCache = this.typeNow
      this.worldBase.on('mouseover', function (d) {
        const x = d3.event.clientX
        const y = d3.event.clientY
        const countryName = d.properties.name
        // 某一个国家的所有数据
        const OneCountryData = dataCache.filter(d => d.country === countryName)
        // 某一个国家某一天的数据
        let count = 0
        if (OneCountryData.length > 0) {
          OneCountryData[0].list.map(d => {
            if (d.date === dateCache) {
              if (typeNowCache === 'total_confirm') {
                count = d.total_confirm
              } else if (typeNowCache === 'daily_confirm') {
                count = d.daily_confirm
              } else if (typeNowCache === 'total_death') {
                count = d.total_death
              } else if (typeNowCache === 'daily_death') {
                count = d.daily_death
              } else if (typeNowCache === 'total_cure') {
                count = d.total_cure
              } else if (typeNowCache === 'daily_cure') {
                count = d.daily_cure
              } else if (typeNowCache === 'cure_rate') {
                count = d.cure_rate
              } else if (typeNowCache === 'death_rate') {
                count = d.death_rate
              }
            }
          })
        }
        d3.select('.tooltip')
          .attr('transform', `translate(${x},${y})`) // 提示框跟随鼠标移动
          .attr('opacity', 0.8)
        d3.select('.tooltip').select('text')
          .text(countryName + ' : ' + count)
          .attr('text-anchor', 'start')
          .attr('font-size', '15')
          // .text(`${d.name} : ${d.value}`)
      })
        .on('mouseout', function () {
          d3.select('.tooltip')
            .attr('opacity', 0)
        })
    },

    reDraw () {
      this.worldBaseInit()
      this.legendChange()
      this.tooltipInit()
    }
  }
}

</script>

<style></style>
