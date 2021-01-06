<template>
  <div>
    <div>{{currentDate}}</div>
    <div>
      <VueSlider
        :value="currentDate"
        @change="emitDateSwitch"
        :data="optionDates"
        :disabled="false"
        :lazy="false"
        :clickable="true"
      />
    </div>
  </div>
</template>

<script>
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/default.css'

export default {
  name: 'DateSlider',
  props: ['startDate', 'endDate', 'currentDate'],
  data: () => {
    return {
      optionDates: []
    }
  },
  components: {
    VueSlider
  },
  mounted () {
    this.calcDateList()
  },
  watch: {
    startDate: function () {
      this.calcDateList()
    },
    endDate: function () {
      this.calcDateList()
    }
  },
  methods: {
    formatString (y, m, d) {
      let year = (1900 + y) + ''
      let month
      if (m < 9) {
        month = '0' + (m + 1)
      } else {
        month = '' + (m + 1)
      }
      let day
      if (d < 10) {
        day = '0' + d
      } else {
        day = '' + d
      }
      return year + '-' + month + '-' + day
    },
    nextDate (oldDate) {
      let ret = new Date(oldDate.valueOf())
      ret.setDate(ret.getDate() + 1)
      return ret
    },
    isAfter (dayToCompare, threshold) {
      if (dayToCompare.getYear() > threshold.getYear()) {
        return true
      } else if (dayToCompare.getYear() === threshold.getYear()) {
        if (dayToCompare.getMonth() > threshold.getMonth()) {
          return true
        } else if (dayToCompare.getMonth() === threshold.getMonth() && dayToCompare.getDate() > threshold.getDate()) {
          return true
        }
      }
      return false
    },
    calcDateList () {
      console.time('calcDateList')
      this.optionDates = []
      let startYear = parseInt(this.startDate.substring(0, 4))
      let startMonth = parseInt(this.startDate.substring(5, 7))
      let startDay = parseInt(this.startDate.substring(8, 10))
      let endYear = parseInt(this.endDate.substring(0, 4))
      let endMonth = parseInt(this.endDate.substring(5, 7))
      let endDay = parseInt(this.endDate.substring(8, 10))
      let iterDate = new Date(startYear, startMonth - 1, startDay)
      let finalDate = new Date(endYear, endMonth - 1, endDay)
      while (true) {
        this.optionDates.push(this.formatString(iterDate.getYear(), iterDate.getMonth(), iterDate.getDate()))
        iterDate = this.nextDate(iterDate)
        if (this.isAfter(iterDate, finalDate) === true) {
          break
        }
      }
      console.timeEnd('calcDateList')
    },
    emitDateSwitch (e) {
      this.$emit('switchDate', e)
    }
  }
}
</script>

<style></style>
