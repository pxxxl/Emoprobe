<template>
    <div id="echart">
        <div id="chart1" class="border"></div>
        <div id="chart2" class="border"></div>
        <div id="chart3" class="border"></div>
        <el-select v-model="ip_select" @change="emo_in_ip_chartChange">
            <el-option v-for="(item,key) in ip"
                :value="key"
                :lable="item"
                :key="item"
            >
        </el-option>
        </el-select>
        <div id="chart4"></div>
    </div>
</template>

<script lang="ts" setup>
import * as echarts from 'echarts';
import {onMounted, ref} from 'vue';

const props = defineProps(['overview',"ipAnalys"]);
const pie_size = 200;
const ip_select = ref(0);

const ip = ref();//ip arrary
const emotion = ref();//emotion arrary
emotion.value = props.ipAnalys.emotion;
ip.value =props.ipAnalys.ip;

const emotionLen = emotion.value.length;
const ipLen = ip.value.length;

const mychart1 = ref();
const mychart2 = ref();
const ip_in_emo_chart = ref();
const emo_in_ip_chart =ref()


const ip_people_num = ref();
const ip_in_emotion_rate = ref();
const emo_in_ip_rate = ref();
ip_people_num.value = props.ipAnalys.num_ip_person;
ip_in_emotion_rate.value = props.ipAnalys.ip_ratio_per_emotion;
emo_in_ip_rate.value = props.ipAnalys.emotion_ratio_per_ip;

const ip_in_emotion_data = (all_data:any[]):any=>{
    let out_put = new Array<object>();
    let x:number = 0;
    let y:number = 0;
    let len:number = all_data.length;
    for(x = 0;x < len; x++){
        let contamp = {
            type:'pie',
            center:[(x % 5) * pie_size + (pie_size/2), pie_size *Math.floor(x / 5.0) + pie_size/2],
            radius:100,
            data:new Array()
        }
        let len = all_data[x].ip.length;
        for(y=0; y<len; y++){
            contamp.data.push({
                name:all_data[x].ip[y],//add name
                value:all_data[x].num_ip[y]//add value
            })
        }
        out_put.push(contamp);//put a chart data in series list
    }
    return out_put;
}

const emo_in_ip_chartChange = ()=>{
    emo_in_ip_chart.value.setOption({
        dataset:{
            source:[
                emo_in_ip_rate.value[ip.value].emotion,
                emo_in_ip_rate.value[ip.value].emotion
            ]
        },
        series:{
            type:'pie',
            seriesLayoutBy:'row',
            center:["50%","50%"],
            encode:{
                itemName:[0],
                value:[1]
            },
        },
    })
}

onMounted(() => {
    mychart1.value = echarts.init(document.getElementById('chart1'),null,{
        width:emotionLen * 100,
        height:100
    });
    mychart1.value.setOption({
        title: {
            text: "评论中各个情感分类的人数"
        },
        xAxis: {
            type: 'category',
            data: props.overview.emotion
        },
        yAxis: {},
        series: {
            type: "bar",
            data: props.overview.num_person
        }
    });

    mychart2.value = echarts.init(document.getElementById('chart2'),null,{
        width:200,
        height:200
    });
    mychart2.value.setOption({
        dataset:{
            source:[ip,ip_people_num]
        },
        series:{
            type:'pie',
            seriesLayoutBy:'row',
            encode:{
                x:[0],
                y:[1]
            }
        }
    });

    ip_in_emo_chart.value = echarts.init(document.getElementById("chart3"),null,{
        width:pie_size * ( (emotionLen >= 5) ? 5 : emotionLen ),
        height:pie_size * ((emotionLen >= 5) ? 2 : 1)
    });
    ip_in_emo_chart.value.setOption({
        series:ip_in_emotion_data(ip_in_emotion_rate.value)
    });

    emo_in_ip_chart.value = echarts.init(document.getElementById("chart4"),null,{
        width:300,
        height:300
    });
    emo_in_ip_chartChange();
})
</script>

<style scoped>

</style>