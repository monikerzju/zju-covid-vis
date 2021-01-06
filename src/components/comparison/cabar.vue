<template>
  <div>
    <div class="title">{{chartTitle}}</div>
  </div>
</template>

<script>
export default {
  name: 'CompareAnimation',
  props: ['chartData'],
  data: () => {
    return {
      chartTitle: '全球新冠疫情动态排行榜'
    }
  }
}
</script>

<style></style>
