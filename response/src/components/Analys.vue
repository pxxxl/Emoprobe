<template>
    <el-button id="backpart" @click="back">
        <el-icon><ArrowLeftBold /></el-icon>
        返回
    </el-button>
    <div id="information">
        <div class="inshow left-float border">视频BV号:<b>{{ video_information.video_bid }}</b></div>
        <div class="inshow left-float border">视频标题:<b>{{ video_information.video_title }}</b></div>
        <div class="inshow left-float border">最后操作时间:<b>{{ video_information.operation_time }}</b></div>
        <div class="inshow left-float border">UP主用户名:<b>{{ video_information.owner_name }}</b></div>
        <div class="inshow left-float border">视频分区:<b>{{ video_information.video_tables }}</b></div>
        <div class="inshow left-float border">发布时间:<b>{{ video_information.pubdate }}</b></div>
        <div class="inshow left-float border">点赞数:<b>{{ video_information.video_like }}</b></div>
        <div class="inshow left-float border">投币数:<b>{{ video_information.video_coin }}</b></div>
        <div class="inshow left-float border">收藏数:<b>{{ video_information.video_favorite }}</b></div>
        <div class="inshow left-float border">分享数:<b>{{ video_information.video_share }}</b></div>
        <div class="inshow left-float border">评论数:<b>{{ video_information.video_reply }}</b></div>
    </div>
    <div id="charts">
        <chart :overview="chartdata[0]" :ipAnalys="chartdata[1]"/>
    </div>
    <div id="table">
        <div class="pagination-block">
            <h1 class="dis-flex center-flex">结果</h1>
            <sift @sift="SiftUpdate"/>
            <div class="demonstration">
                <el-table :data="per_pageCom" style="width: 100%;">
                    <el-table-cloumn prop="user_id" lable="用户id"></el-table-cloumn>
                    <el-table-cloumn prop="user_name" lable="用户名称"></el-table-cloumn>
                    <el-table-cloumn prop="user_ip" lable="用户IP"></el-table-cloumn>
                    <el-table-cloumn prop="user_sex" lable="性别"></el-table-cloumn>
                    <el-table-cloumn prop="comment_data" lable="日期"></el-table-cloumn>
                    <el-table-cloumn prop="comment_text" lable="评论文本"></el-table-cloumn>
                    <el-table-cloumn prop="comment_like" lable="点赞数"></el-table-cloumn>
                    <el-table-cloumn prop="comment_reply" lable="回复数"></el-table-cloumn>
                    <el-table-cloumn prop="emnotion" lable="情感"></el-table-cloumn>
                </el-table>
            </div>
            <el-pagination layout="prev, pager, next" :hide-on-single-page="true" :page-size="30" v-model:page-count="all_pagenum" v-model:current-page="pn" background="blue"/>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { nextTick, onMounted,ref,watch } from 'vue';
import {useRoute,useRouter} from 'vue-router'
import axios, { formToJSON } from 'axios';
import {ShowErrorMessage} from '@/assets/g.js';
import sift from './sift.vue';
import chart from './chart.vue';

const route = useRoute();
const router = useRouter();
const api = '/api/v1/videos/page/filter';
const overviewurl = '/api/v1/videos/statistics/overview';
const ipAnalysurl = '/api/v1/videos/statistics/ip';

const per_pageCom = ref([]);
const all_pagenum = ref(1);
const page_len = 30;
const video_information = ref({});
const bv = ref(route.query.bv.toString());
const pn=ref(1);

const ip = ref("");
const gender = ref("");
const date = ref("");
const like = ref("");
const reply = ref("");
const emotion = ref("");

const chartdata=ref(new Array(2));

interface Params{
    bv:string,
    autopost:number,
    n_per_page:number,
    pn:number,
    user_ip:string,
    user_sex:string,
    comment_date:string,
    comment_like:string,
    comment_reply:string,
    emotion:string
}

const back = ()=>{
    router.push({
        path:"/"
    });
}

const get_page_comment = (bvString:string,autopost:number,pageLen:number,page:number,ip_sift?:string,sex_sift?:string,date_sift?:string,like_sift?:string,reply_sift?:string,emotion_sift?:string)=>{
    let params:Params = {} as Params;
    params.bv =bvString;
    params.autopost = autopost;
    params.n_per_page = pageLen;
    params.pn = page;

    if(ip_sift && ip_sift != "")params.user_ip = ip_sift;
    if(sex_sift && sex_sift != "")params.user_sex = sex_sift;
    if(date_sift && date_sift != "")params.comment_date = date_sift;
    if(like_sift && like_sift != "")params.comment_like = like_sift;
    if(reply_sift && reply_sift != "")params.comment_reply = reply_sift;
    if(emotion_sift && emotion_sift != "")params.emotion = emotion_sift;

    axios.get(api,{
        params:params
    }).then((org_response:any)=>{
        let response:any = JSON.parse(org_response.data);
        if(response.code == 408 || response.code == 408){
            ShowErrorMessage(response.msg + " 即将跳转");
            // setTimeout(back,3000);
        }
        all_pagenum.value = response.data.total_page_num;
        per_pageCom.value = response.data.comments;
        video_information.value = response.data.video;
    }).catch((error:any)=>{
        ShowErrorMessage(error + " 服务器链接错误，即将跳转");
        // setTimeout(back,3000);
    });
}

const SiftUpdate = (ip_rq:string,gender_rq:string,date_rq:string,like_rq:string,reply_rq:string,emotion_rq:string)=>{
    console.log(ip_rq);
    console.log(gender_rq);
    console.log(date_rq);
    console.log(like_rq);
    console.log(reply_rq);
    console.log(emotion_rq);

    pn.value = 1;
    ip.value = ip_rq;
    gender.value = date_rq;
    date.value = date_rq;
    like.value = like_rq;
    reply.value = reply_rq;
    emotion.value = emotion_rq;

    get_page_comment(bv.value,1,
        page_len,
        pn.value  - 1,
        ip.value,
        gender.value,
        date.value,
        like.value,
        reply.value,
        emotion.value
    );
}

const GetChartData = (url:string,x:number)=>{
    axios.get('/api/v1/videos/statistics/overview',{
        params:{
            bv:bv.value
        }
    }).then((org_response)=>{
        let response =JSON.parse(org_response.data);
        chartdata.value[0] = response.data;
    }).catch((error)=>{
        ShowErrorMessage(error + " 获取统计图数据出错")
    })
}

onMounted(()=>{
    get_page_comment(bv.value,1,page_len,pn.value-1);//get the first page and total page
    GetChartData(overviewurl,0);//get the overview data from backside
    GetChartData(ipAnalysurl,1);//get all the ip analys data from backside
});

watch(pn,(New_pn)=>{
    get_page_comment(bv.value,
        1,
        page_len,
        pn.value-1,
        ip.value,
        gender.value,
        date.value,
        like.value,
        reply.value,
        emotion.value
    );//get the first page and total page
});

</script>

<style scoped>
.inshow{
    margin: 2vh;
    padding: 1vh;
    border-radius: 2vh;
    font-size: large;
    background-color: var(--color-tag);
    overflow: hidden;
}

#information{
    width: 100%;
    overflow: hidden;
}

#table{
    /* clear: both; */
    width: 100%;
}
</style>