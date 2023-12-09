<template>
    <div id="echart">
        <div id="chart1"></div>
        <div id="chart2"></div>
        <div id="chart3">
        </div>
        <!-- <div id="chart4">
            <div class="ip-in-emotion" v-for="item in emotion"></div>
        </div> -->
    </div>
</template>

<script lang="ts" setup>
import * as echarts from 'echarts';
import {onMounted,ref} from 'vue';

// const props = defineProps(['overview',"ipAnalys"]);

// const ip = ref(props.ipAnalys.ip);
// const emotion = ref(props.ipAnalys.emotion);

// const ip_total_rate = ref(props.ipAnalys.num_ip_person);
// const emo_in_ip_rate = ref(props.ipAnalys.emotion_ratio_per_ip);
// const ip_in_emotion_rate = ref(props.ipAnalys.ip_ratio_per_emotion);

// const mychart1 = echarts.init(document.getElementById('chart1'));
// const mychart2 = echarts.init(document.getElementById('chart2'));
// const emo_in_ip_chart = echarts.init(document.getElementById("chart3"));


// mychart1.setOption({
//     title:{
//         text:"评论中各个情感分类的人数"
//     },
//     xAxis:{
//         type:'category',
//         data:props.overview.emotion
//     },
//     yAxis:{},
//     series:{
//         type:"bar",
//         data:props.overview.num_person
//     }
// });

// mychart2.setOption({
//     title:"所有评论中各ip的占比",
//     series:{
//         type:"pie",
//         data:{
//             name:['sada','asd','dgsgdfg','dfgdfdf'],
//             value:[12,23,34,34]
//         }
//     }
// });

// emo_in_ip_chart.setOption({
//     dataset:{
//         source:[]
//     }
// })


onMounted(() => {
})
</script>

<style scoped>
#chart1{
    width: 30vh;
    height: 50vh;
}

#chart2{
    width: 30vh;
    height: 50vh;
}
</style>