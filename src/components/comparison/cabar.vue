<template>
  <div>
    <meta charset="utf-8">
    <div class="title">{{chartTitle}}</div>
    <div>
      <DateSlider
        :startDate='firstDate'
        :endDate='lastDate'
        :currentDate='date'
        @switchDate='switchDate'
      />
    </div>
    <div id="cabar-container" :style="{width:'document.body.clientWidth',height:600}" >
      <meta name='viewport' content='width=device-width initial-scale=1.0' />
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'
import DateSlider from '../common/slider.vue'

export default {
  name: 'CompareAnimation',
  props: ['chartData'],
  components: {
    DateSlider
  },
  data: () => {
    return {
      chartTitle: '全球新冠疫情动态排行榜',
      svg: null,
      // For the Slider
      firstDate: '2020-03-12',
      lastDate: '2020-03-28',
      date: '2020-03-12',
      dateChange: null,
      dateChangeFlag: false,
      dataOri: [
        ['国家或地区', '2020-03-12', '2020-03-13', '2020-03-14', '2020-03-15', '2020-03-16', '2020-03-17', '2020-03-18', '2020-03-19', '2020-03-20', '2020-03-21', '2020-03-22', '2020-03-23', '2020-03-24', '2020-03-25', '2020-03-26', '2020-03-27', '2020-03-28'],
        ['美国', '1561', '14153', '84080', '244593', '464442', '669272', '871617', '1072667', '1261409', '1423726', '1584486', '1730259', '1878543', '2023590', '2191052', '2422299', '2510281'],
        ['巴西', '52', '621', '2985', '8044', '18092', '30425', '50036', '87187', '135773', '203165', '310087', '438238', '614941', '802828', '978142', '1228114', '1313667'],
        ['俄罗斯', '28', '199', '840', '3548', '10131', '27938', '62773', '106498', '177160', '252245', '317554', '379051', '440538', '501800', '560321', '613148', '626779'],
        ['印度', '73', '194', '727', '2543', '6725', '13430', '23077', '34863', '56351', '81997', '118226', '165386', '226713', '297535', '380532', '490401', '528859'],
        ['英国', '456', '2689', '11658', '33718', '65077', '103093', '138078', '171253', '206715', '233151', '250908', '269127', '281661', '291409', '300469', '307980', '311727'],
        ['秘鲁', '15', '234', '580', '1414', '5256', '12491', '20914', '36976', '58526', '80604', '108769', '141779', '183198', '214788', '244388', '268602', '275989'],
        ['智利', '23', '238', '1306', '3404', '5972', '8807', '11812', '16023', '24581', '37040', '57581', '86943', '118292', '154092', '225103', '259064', '267766'],
        ['西班牙', '2277', '17963', '57786', '112065', '153222', '184948', '213024', '213435', '221447', '229540', '233037', '237906', '240660', '242707', '245268', '247486', '248469'],
        ['意大利', '15113', '41035', '80589', '115242', '143626', '168941', '189973', '205463', '215858', '223096', '228006', '231732', '234013', '236142', '238159', '239706', '240136'],
        ['伊朗', '10075', '18407', '29406', '50468', '66220', '77995', '87026', '94640', '103135', '114533', '129341', '143849', '164270', '180156', '197647', '215096', '220180'],
        ['墨西哥', '12', '164', '585', '1510', '3441', '6297', '11633', '19224', '29616', '42595', '59567', '81400', '105680', '133974', '165455', '202951', '212802'],
        ['巴基斯坦', '28', '501', '1373', '2686', '4695', '7025', '11940', '18114', '26435', '38799', '50694', '64028', '89249', '125933', '165062', '195745', '202955'],
        ['土耳其', '1', '192', '3629', '18135', '42282', '74193', '101790', '120204', '133721', '144749', '153548', '160979', '167410', '174023', '184031', '193115', '195883'],
        ['德国', '2078', '15320', '43938', '84794', '118181', '137698', '153129', '163009', '169430', '174478', '179021', '182196', '184472', '186691', '189817', '193371', '194458'],
        ['法国', '2281', '10871', '29155', '59105', '86334', '144944', '157026', '165764', '173040', '176712', '179306', '183309', '185986', '188354', '190107', '191288', '199473'],
        ['沙特', '45', '274', '1012', '1885', '3287', '6380', '13930', '22753', '33731', '46869', '65077', '80185', '93157', '116021', '145991', '170639', '178504'],
        ['孟加拉国', '3', '17', '44', '56', '330', '1572', '4186', '7667', '12425', '18863', '28511', '40321', '57563', '78052', '102292', '126606', '133978'],
        ['南非', '17', '150', '927', '1462', '1934', '2605', '3953', '5647', '8232', '12739', '19137', '27403', '40792', '58568', '83890', '118375', '131800'],
        ['加拿大', '117', '800', '4042', '11284', '20654', '30809', '43299', '54457', '66201', '74781', '82742', '89976', '95269', '99159', '101877', '104463', '104878'],
        ['卡塔尔', '262', '460', '549', '949', '2376', '4103', '7764', '13409', '18890', '28272', '38651', '50914', '63741', '75071', '84441', '91838', '93663'],
        ['中国', '80813', '80967', '81340', '81620', '81907', '82692', '82804', '82874', '82886', '82933', '82971', '82995', '84614', '84659', '84940', '85148', '84743'],
        ['日本', '639', '924', '1387', '2495', '4667', '8626', '12368', '14088', '15477', '16120', '16424', '16598', '16911', '17187', '17588', '18055', '18268'],
        ['韩国', '7869', '8565', '9241', '9976', '10423', '10613', '10708', '10774', '10822', '11018', '11142', '11402', '11668', '12003', '12306', '12602', '12715']
      ]
    }
  },

  mounted () {
    this.cabarInit()
  },

  methods: {
    cabarInit () {
      console.log(this.dataOri)
      const width = document.body.clientWidth
      const height = 600
      const margin = {top: 20, bottom: 0, left: 50, right: 100}
      const chartWidth = width - (margin.left + margin.right)
      const chartHeight = height - (margin.top + margin.bottom)
      const data = []
      const count = 10
      const duration = 500
      const barPadding = 20
      const barHeight = (chartHeight - (barPadding * count)) / count
      const getDate = () => this.dataOri[0][dateIndex]
      let dateIndex = 0
      let date = getDate()
      let dataSlice = []
      let chart = null
      let scale = null
      let axis = null
      let svg = null
      let dateTitle = null
      let dataOriNow = this.dataOri
      let dateNow = this.date
      console.log('dateNow:  ' + dateNow)
      console.log('this.date:  ' + this.date)

      // 创建SVG
      const createSvg = () => (svg = d3.select('#cabar-container').append('svg').attr('width', width).attr('height', height))

      // 格式化数据
      const formatData = () => {
        dataOriNow[0].forEach((date, index) => {
          if (index > 0) {
            dataOriNow.forEach((row, rowIndex) => {
              if (rowIndex > 0) {
                data.push({
                  name: row[0],
                  value: Number(row[index]),
                  lastValue: index > 1 ? Number(row[index - 1]) : 0,
                  date: date,
                  color: randomRgbColor()
                })
              }
            })
          }
        })
      }

      // 获取当天数据并按倒叙排列
      const sliceData = () =>
        (dataSlice = (data.filter(d => d.date === date).sort((a, b) => b.value - a.value).slice(0, count)))

      // 创建比例尺
      const createScale = () =>
        (scale = (d3.scaleLinear().domain([0, d3.max(dataSlice, d => d.value)]).range([0, chartWidth])))

      // 创建坐标轴
      const renderAxis = () => {
        createScale()

        axis = (d3.axisTop().scale(scale).ticks(5).tickPadding(10).tickSize(0))

        svg.append('g')
          .classed('axis', true)
          .style('transform', `translate3d(${margin.left}px, ${margin.top}px, 0)`)
          .call(axis)
      }

      // 创建坐标线
      const renderAxisLine = () => {
        d3.selectAll('g.axis g.tick').select('line.grid-line').remove()
        d3.selectAll('g.axis g.tick').append('line')
          .classed('grid-line', true)
          .attr('stroke', 'black')
          .attr('x1', 0)
          .attr('y1', 0)
          .attr('x2', 0)
          .attr('y2', chartHeight)
      }

      // 当数据变化时更新坐标轴
      const updateAxis = () => {
        createScale()

        axis.scale().domain([0, d3.max(dataSlice, d => d.value)])

        svg.select('g.axis')
          .transition().duration(duration).ease(d3.easeLinear)
          .call(axis)

        d3.selectAll('g.axis g.tick text').attr('font-size', 14)
      }

      // 渲染日期标题
      const renderDateTitle = () => {
        dateTitle = svg.append('text')
          .classed('date-title', true)
          .text(date)
          .attr('x', chartWidth - margin.top)
          .attr('y', chartHeight - margin.left)
          .attr('fill', 'rgb(128, 128, 128)')
          .attr('font-size', 40)
          .attr('text-anchor', 'end')
      }

      const calTranslateY = (i, end) => {
        if (dateIndex === 1 || end) {
          return (barHeight + barPadding) * i + (barPadding / 2)
        } else {
          return (barHeight + barPadding) * (count + 1)
        }
      }

      const createChart = () => {
        chart = svg.append('g')
          .classed('chart', true)
          .style('transform', `translate3d(${margin.left}px, ${margin.top}px, 0)`)
      }

      const renderChart = () => {
        const bars = chart.selectAll('g.bar').data(dataSlice, (d) => d.name)

        let barsEnter

        barsEnter = bars.enter()
          .append('g')
          .classed('bar', true)
          .style('transform', (d, i) => `translate3d(0, ${calTranslateY(i)}px, 0)`)

        dateIndex > 1 && barsEnter
          .transition().duration(this.duration)
          .style('transform', (d, i) => `translate3d(0, ${calTranslateY(i, 'end')}px, 0)`)

        barsEnter.append('rect')
          .style('width', d => scale(d.value))
          .style('height', barHeight + 'px')
          .style('fill', d => d.color)

        barsEnter.append('text')
          .classed('label', true)
          .text(d => d.name)
          .attr('x', '-5')
          .attr('y', barPadding)
          .attr('font-size', 14)
          .style('text-anchor', 'end')

        barsEnter.append('text')
          .classed('value', true)
          .text(d => d.value)
          .attr('x', d => scale(d.value) + 10)
          .attr('y', barPadding)

        // 更新模式
        bars.transition().duration(duration).ease(d3.easeLinear)
          .style('transform', (d, i) => 'translate3d(0, ' + calTranslateY(i, 'end') + 'px, 0)')
          .select('rect')
          .style('width', d => scale(d.value) + 'px')

        bars
          .select('text.value')
          .transition().duration(duration).ease(d3.easeLinear)
          .attr('x', d => scale(d.value) + 10)
          .tween('text', function (d) {
            const textDom = this
            const i = d3.interpolateRound(d.lastValue, d.value)
            return (t) => (textDom.textContent = i(t))
          })

        // 退出模式
        bars.exit()
          .transition().duration(duration).ease(d3.easeLinear)
          .style('transform', function (d, i) {
            return 'translate3d(0, ' + calTranslateY(i) + 'px, 0)'
          })
          .style('width', function (d) {
            return scale(d.value) + 'px'
          })
          .remove()
      }

      function createTicker () {
        const ticker = d3.interval(() => {
          if (dateIndex < dataOriNow[0].length - 1) {
            dateIndex++
            date = getDate()
            dateTitle.text(date)
            sliceData()
            updateAxis()
            renderAxisLine()
            renderChart()
          } else {
            ticker.stop()
          }
        }, duration)
      }

      const init = () => {
        createSvg() // 创建画布
        formatData() // 格式化数据
        sliceData() // 截取当天数据
        renderAxis() // 渲染坐标轴
        renderAxisLine() // 渲染指示线
        renderDateTitle() // 渲染日期
        createChart() // 创建图表
        renderChart() // 渲染图表
        createTicker() // 创建定时器
      }

      init()

      function randomRgbColor () {
        const r = Math.floor(Math.random() * 256)
        const g = Math.floor(Math.random() * 256)
        const b = Math.floor(Math.random() * 256)
        return `rgb(${r},${g},${b})`
      }
    },

    async switchDate (opt) {
      this.date = opt
    }
  }
}
</script>

<style></style>
