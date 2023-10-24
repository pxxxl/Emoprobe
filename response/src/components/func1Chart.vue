<template>
<p>data</p>
<div class="echarts-box">
    <div id="myEcharts" :style="{ width: '900px', height: '300px' }">
    <!-- data chart show -->
    </div>
</div>
<div id="comment-show">
<!-- PUT COMMENT DATA -->
  <table id="table">
    <tr id="head" class="com-width">
      <th>名字</th>
      <th>IP地址</th>
      <th>性别</th>
      <th>日期</th>
      <th>评论内容</th>
      <th>喜恶</th>
      <th>回复</th>
      <th>情感</th>
    </tr>
    <tr v-for="(item,index) of comment_arr" v-bind:key="index" class="com-width">
      <td>
        {{item.user_name}}
      </td>
      <td>
        {{ item.user_ip }}
      </td>
      <td>
        {{item.user_sex}}
      </td>
      <td>
        {{ item.comment_date }}
      </td>
      <td>
        {{ item.comment_text }}
      </td>
      <td>
        {{ item.comment_like }}
      </td>
      <td>
       {{  item.comment_reply}}
      </td>
      <td>
        {{item.comment_emotion}}
      </td>
    </tr>
  </table>
  
</div>
</template>

<script>
import * as echarts from 'echarts';
export default{
    mounted() {
      //  this.initChart();
    },
    unmounted() {
        // echarts.dispose;
    },
    props:['comment_arr','chart_data'],
    methods: {
      // TODO
    }
}
</script>
<style scoped>
#head{
  user-select: none;
}

#table{
  margin: auto;
  height: auto;
  width: 100vh;
}

.com-width{
  width: auto;
}
</style>