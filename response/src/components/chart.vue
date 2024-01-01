<template>
    <div id="echart">
        <div id="chart1" class="" :style=" {boxShadow:`var(--el-box-shadow-dark)`,margin:50}"></div>
        <el-divider border-style="double" />
        <div id="chart2" class="" :style=" {boxShadow:`var(--el-box-shadow-dark)`}"></div>
        <el-divider border-style="double" />
        <div id="chart3" class="" :style=" {boxShadow:`var(--el-box-shadow-dark)`}"></div>
        <el-divider border-style="double" />
        <el-select v-model="ip_select" @change="emo_in_ip_chartChange">
            <el-option v-for="(item,key) in ip"
                :value="key"
                :label="item"
            >
            </el-option>
        </el-select>
        <div id="chart4" class="" :style=" {boxShadow:`var(--el-box-shadow-dark)`}"></div>
        <el-divider border-style="double" />
        <div id="chart5"  :style=" {boxShadow:`var(--el-box-shadow-dark)`}"></div>

    </div>
</template>

<script lang="ts" setup>
import axios from 'axios';
import * as echarts from 'echarts';
import {onMounted, ref} from 'vue';

const props = defineProps(['overview',"ipAnalys"]);
const pie_size = 400;
const ip_select = ref(0);

const ip = ref();//ip arrary
const emotion = ref();//emotion arrary

const emotionLen = ref();
const ipLen = ref();

const mychart1 = ref();
const mychart2 = ref();
const ip_in_emo_chart = ref();
const emo_in_ip_chart =ref();
const geography_chart_china = ref();


const ip_people_num = ref();
const ip_in_emotion_rate = ref();
const emo_in_ip_rate = ref();

const ip_in_emotion_data = (all_data:any):any=>{
    // console.log(all_data.ip);
    let out_put = new Array<object>();
    let x:number = 0;
    let y:number = 0;
    for(x = 0;x < emotionLen.value; x++){
        let contamp = {
            name:emotion.value[x],
            type:'pie',
            center:[(x % 3.0) * pie_size + (pie_size/2), pie_size *Math.floor(x / 3.0) + pie_size/2],
            radius:[0,100],
            data:new Array(),
            label:{
                show:true,
                formatter:"{b}: {d}%",
                alignTo:"labelLine"
            },
            tooltip:{
            },
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

const ip_in_emotion_title = ()=>{
    let out_put = new Array<object>();
    emotion.value.forEach((element,index) => {
        out_put.push({
            text:element,
            left: (index % 3)*pie_size + (pie_size/2),
            top: pie_size *Math.floor(index / 3.0) + 50,
            textAlign:'center'
        })
    });
    return out_put;
}

const emo_in_ip_chartChange = ()=>{
    emo_in_ip_chart.value.setOption({
        tooltip:{
            trigger:'item'
        },
        dataset:{
            source:[
                emo_in_ip_rate.value.emotion[ip_select.value],
                emo_in_ip_rate.value.num_emotion[ip_select.value]
            ]
        },
        title:{
            text:"每个ip里的情感比例",
            padding:[5, 15]
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
            tooltip:{
                formatter:"{c}"
            }
        },
    })
}

const get_IP_num=(province:string):number=>{
    let key:number = ip.value.indexOf(province);
    if(key === -1)return 0;
    else{
        return ip_people_num .value[key];
    }
}

onMounted(() => {
    emotion.value = props.ipAnalys.emotion;
    ip.value =props.ipAnalys.ip;
    ipLen.value = ip.value.length;
    emotionLen.value = emotion.value.length;
    // console.log(props.ipAnalys);
    // console.log(props.overview);

    ip_people_num.value = props.ipAnalys.num_ip_person;
    ip_in_emotion_rate.value = props.ipAnalys.ip_ratio_per_emotion;
    emo_in_ip_rate.value = props.ipAnalys.emotion_ratio_per_ip;

    mychart1.value = echarts.init(document.getElementById('chart1'),null,{
        width:emotionLen.value * 200,
        height:300
    });
    mychart1.value.setOption({
        title: {
            text: "评论中各个情感分类的人数",
            padding:[5, 15]
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
        tooltip:{
            trigger:'item'
        },
        title:{
            text:"视频评论的Ip占比",
            padding:[5, 15]
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
        width:pie_size * ( (emotionLen.value >= 3) ? 3 : emotionLen.value ),
        height:pie_size * ((emotionLen.value > 3) ? 2 : 1)
    });
    ip_in_emo_chart.value.setOption({
        tooltip:{
            trigger:'item'
        },
        title:ip_in_emotion_title(),
        series:ip_in_emotion_data(ip_in_emotion_rate.value),
    });

    emo_in_ip_chart.value = echarts.init(document.getElementById("chart4"),null,{
        width:500,
        height:300
    });
    emo_in_ip_chartChange();

    geography_chart_china.value = echarts.init(document.getElementById('chart5'),null,{
        width:1000,
        height:500
    });
    axios.get('/resource/map/china.json')
    .then((org_response)=>{
        echarts.registerMap('topo', {geoJSON: org_response.data});
        geography_chart_china.value.setOption({
            title:{
                text:"Ip地理分布图",
                padding:[5, 15]
            },
            dataRange:{
                x:'left',
                y:'bottom',
                splitList:[
                    {start:1000,label:'1000以上',color:'rgba(50,0,0,0.8)'},
                    {start:101,end:1000,label:'101-1000',color:'rgba(150,0,0,0.8)'},
                    {start:50,end:101,label:'50-100',color:'rgba(255,0,0,0.8)'},
                    {start:41,end:50,label:'41-50',color:'rgba(255,0,0,0.7)'},
                    {start:31,end:40,label:'31-40',color:'rgba(255,0,0,0.6)'},
                    {start:21,end:30,label:'21-30',color:'rgba(255,0,0,0.4)'},
                    {start:5,end:20,label:'5-20',color:'rgba(255,0,0,0.2)'},
                    {start:0,end:4,label:'0-4',color:'rgba(255,255,255,1)'},
                ]
            },
            series: [{
                colorBy:'data',
                type: 'map',
                map: 'topo',
                layoutSize:'100%',
                data: [{ name: "北京市", value: get_IP_num('北京')},
                    { name: "天津市", value: get_IP_num('天津') },
                    { name: "河北省", value: get_IP_num("河北") },
                    { name: "山西省", value: get_IP_num("山西") },
                    { name: "内蒙古自治区", value: get_IP_num("内蒙") },
                    { name: "辽宁省", value: get_IP_num("辽宁") },
                    { name: "吉林省", value: get_IP_num("吉林") },
                    { name: "黑龙江省", value: get_IP_num("黑龙江") },
                    { name: "上海市", value: get_IP_num("上海") },
                    { name: "江苏省", value: get_IP_num("江苏") },
                    { name: "浙江省", value: get_IP_num("浙江") },
                    { name: "安徽省", value: get_IP_num("安徽") },
                    { name: "福建省", value: get_IP_num("福建") },
                    { name: "江西省", value: get_IP_num("江西") },
                    { name: "山东省", value: get_IP_num("山东") },
                    { name: "河南省", value: get_IP_num("河南") },
                    { name: "湖北省", value: get_IP_num("湖北") },
                    { name: "湖南省", value: get_IP_num("湖南") },
                    { name: "重庆市", value: get_IP_num("重庆") },
                    { name: "四川省", value: get_IP_num("四川") },
                    { name: "贵州省", value: get_IP_num("贵州") },
                    { name: "云南省", value: get_IP_num("云南") },
                    { name: "西藏自治区", value: get_IP_num("西藏") },
                    { name: "陕西省", value: get_IP_num("陕西") },
                    { name: "甘肃省", value: get_IP_num("甘肃") },
                    { name: "青海省", value: get_IP_num("青海") },
                    { name: "宁夏回族自治区", value: get_IP_num("宁夏") },
                    { name: "新疆维吾尔自治区", value: get_IP_num("新疆") },
                    { name: "广东省", value: get_IP_num("广东") },
                    { name: "广西壮族自治区", value: get_IP_num("广西") },
                    { name: "海南省", value: get_IP_num("海南") },
                    { name: "台湾省", value: get_IP_num("中国台湾") },
                    { name: "香港特别行政区", value: get_IP_num("中国香港") },
                    { name: "澳门特别行政区", value: get_IP_num("中国澳门") },
                ],
                label:{
                    show:false,
                    position: 'top',
                    formatter:"{b}:{c}"
                },
            }]
        })
    })

})
</script>

<style scoped>
#chart5 canvas{
    border: 0.5px black;
}

</style>