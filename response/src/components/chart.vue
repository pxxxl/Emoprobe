<template>
    <div id="echart">
        <div id="chart1" class="border"></div>
        <div id="chart2" class="border"></div>
        <div id="chart3" class="border"></div>
        <el-select v-model="ip_select" @change="emo_in_ip_chartChange">
            <el-option v-for="(item,key) in ip"
                :value="key"
                :label="item"
            >
        </el-option>
        </el-select>
        <div id="chart4" class="border"></div>
    </div>
</template>

<script lang="ts" setup>
import * as echarts from 'echarts';
import {onMounted, ref} from 'vue';

const props = defineProps(['overview',"ipAnalys"]);
const pie_size = 500;
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

const ip_in_emotion_data = (all_data:any):any=>{
    console.log(all_data.ip);
    let out_put = new Array<object>();
    let x:number = 0;
    let y:number = 0;
    for(x = 0;x < emotionLen; x++){
        let contamp = {
            type:'pie',
            center:[(x % 3.0) * pie_size + (pie_size/2), pie_size *Math.floor(x / 3.0) + pie_size/2],
            radius:[0,100],
            data:new Array(),
            label:{
                show:true,
                formatter:"{b}: {d}%",
                alignTo:"labelLine"
            }
        }
        let len = all_data.ip[x].length;
        for(y=0; y<len; y++){
            contamp.data.push({
                name:all_data.ip[x][y],//add name
                value:all_data.num_ip[x][y]//add value
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
                emo_in_ip_rate.value.emotion[ip_select.value],
                emo_in_ip_rate.value.num_emotion[ip_select.value]
            ]
        },
        title:{
                text:"每个ip里的情感比例"
        },
        series:{
            type:'pie',
            seriesLayoutBy:'row',
            center:["50%","50%"],
            radius:[0,"50%"],
            encode:{
                itemName:[0],
                value:[1]
            },
            label:{
                show:true,
                formatter:"{b}: {d}%",
                alignTo:"labelLine"
            },
        },
    })
}

onMounted(() => {
    mychart1.value = echarts.init(document.getElementById('chart1'),null,{
        width:emotionLen * 200,
        height:300
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
        width:1000,
        height:600
    });
    mychart2.value.setOption({
        title:{
            text:"视频评论的Ip占比"
        },
        dataset:{
            source:[ip.value,ip_people_num.value]
        },
        series:{
            type:'pie',
            center:["50%","50%"],
            radius:[0,"50%"],
            seriesLayoutBy:'row',
            encode:{
                itemName:[0],
                value:[1]
            },
            label:{
                show:true,
                formatter:"{b}: {d}%",
                alignTo:"labelLine"
            }
        }
    });

    ip_in_emo_chart.value = echarts.init(document.getElementById("chart3"),null,{
        width:pie_size * ( (emotionLen >= 3) ? 3 : emotionLen ),
        height:pie_size * ((emotionLen > 3) ? 2 : 1)
    });
    ip_in_emo_chart.value.setOption({
        series:ip_in_emotion_data(ip_in_emotion_rate.value)
    });

    emo_in_ip_chart.value = echarts.init(document.getElementById("chart4"),null,{
        width:500,
        height:300
    });
    emo_in_ip_chartChange();
})
</script>

<style scoped>

</style>