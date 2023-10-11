<template>
<p>这是图标一</p>
<div class="echarts-box">
    <div id="myEcharts" :style="{ width: '900px', height: '300px' }"></div>
</div>
<div id="comment-show">
<!-- PUT COMMENT DATA -->
<!-- 
  <table>
    <tr>
      <th>名字</th>
      <th>IP地址</th>
      <th>性别</th>
      <th>日期</th>
      <th>评论内容</th>
      <th>喜恶</th>
      <th>回复</th>
      <th>情感</th>
    </tr>
    <tr v-for="(item,index) of comment_arr" v-bind:key="index">
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
   -->
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