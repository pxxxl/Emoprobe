<template>
    <el-button id="backpart" @click="back">
        <el-icon><ArrowLeftBold /></el-icon>
        返回
    </el-button>
    <div id="information" v-if="datashow_flag">
        <div class="inshow left-float border">视频BV号:<b>{{ video_information.video_bid }}</b></div>
        <div class="inshow left-float border">视频标题:<b>{{ video_information.video_title }}</b></div>
        <div class="inshow left-float border">最后操作时间:<b>{{ video_information.operation_time }}</b></div>
        <div class="inshow left-float border">UP主用户名:<b>{{ video_information.owner_name }}</b></div>
        <div class="inshow left-float border">视频分区:<b>{{ video_information.video_tables }}</b></div>
        <div class="inshow left-float border">发布时间:<b>{{ video_information.video_pubdate }}</b></div>
        <div class="inshow left-float border">点赞数:<b>{{ video_information.video_like }}</b></div>
        <div class="inshow left-float border">投币数:<b>{{ video_information.video_coin }}</b></div>
        <div class="inshow left-float border">收藏数:<b>{{ video_information.video_favorite }}</b></div>
        <div class="inshow left-float border">分享数:<b>{{ video_information.video_share }}</b></div>
        <div class="inshow left-float border">评论数:<b>{{ video_information.video_reply }}</b></div>
        <div class="inshow left-float border">视频简介:{{video_information.video_desc}}</div>
    </div>
    <div id="charts">
        <h1 class="dis-flex center-flex">评论统计结果</h1>
        <div v-loading="!(chartshow0_flag&&chartshow1_flag)" style="height: 200px;width: 100%;" v-if="!(chartshow0_flag&&chartshow1_flag)"></div>
        <chart :overview="chartdata[0]" :ipAnalys="chartdata[1]" v-if="chartshow0_flag && chartshow1_flag" />
    </div>
    <div id="table">
        <div class="pagination-block">
            <h1 class="dis-flex center-flex">评论分析结果</h1>
            <sift @sift="SiftUpdate" v-if="datashow_flag"/>
            <div class="demonstration">
                <div class="dis-flex center-flex pagecount">
                    <el-pagination layout="prev, pager, next" style="width: 50vh;" :hide-on-single-page="true" :page-size="page_len" v-model:page-count="all_pagenum" v-model:current-page="pn" background="blue"/>
                </div>
                <div v-loading="!datashow_flag" style="height: 200px;width: 100%;" v-if="!datashow_flag"></div>
                <el-table :data="per_pageCom" style="width: 100%;" v-if="datashow_flag" :border="true">
                    <el-table-column prop="user_uid" label="用户id" align="center" min-width="100"></el-table-column>
                    <el-table-column prop="user_name" label="用户名称" align="center"></el-table-column>
                    <el-table-column prop="user_ip" label="用户IP" align="center"></el-table-column>
                    <el-table-column prop="user_sex" label="性别" align="center"></el-table-column>
                    <el-table-column prop="comment_date" label="日期" align="center"></el-table-column>
                    <el-table-column prop="comment_text" label="评论文本" align="center" min-width="500"></el-table-column>
                    <el-table-column prop="comment_like" label="点赞数" align="center"></el-table-column>
                    <el-table-column prop="comment_reply" label="回复数" align="center"></el-table-column>
                    <el-table-column prop="emotion" label="情感" align="center"></el-table-column>
                </el-table>
            </div>
        </div>
    </div>
    {{}}
</template>

<script lang="ts" setup>
import { nextTick, onMounted,ref,watch } from 'vue';
import {useRoute,useRouter} from 'vue-router'
import axios, { formToJSON } from 'axios';
import {ShowErrorMessage} from '@/assets/g.js';
import sift from './sift.vue';
import chart from './chart.vue';
import { Loading } from 'element-plus/es/components/loading/src/service';

const route = useRoute();
const router = useRouter();
const api = '/api/v1/videos/page/filter';
const overviewurl = '/api/v1/videos/statistics/overview';
const ipAnalysurl = '/api/v1/videos/statistics/ip';

const per_pageCom = ref();
const all_pagenum = ref(1);
const page_len = 20;
const video_information = ref();
const bv = ref();
const pn=ref(1);
bv.value = route.query.bv.toString();
video_information.value = {
    video_bid:null,
    video_title:null,
    operation_time:null,
    owner_name:null,
    video_tables:null,
    video_pubdate:null,
    video_like:null,
    video_coin:null,
    video_favorite:null,
    video_share:null,
    video_reply:null//11
}

const chartshow0_flag = ref(false);
const chartshow1_flag = ref(false);
const datashow_flag = ref(false);
const set_time_circle = ref();

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
        let response:any = org_response.data;
        if(response.code == 408 || !response){
            ShowErrorMessage(response.msg + " 即将跳转");
            // setTimeout(back,5000);
        }
        all_pagenum.value = response.data.total_page_num;
        per_pageCom.value = response.data.comments;
        video_information.value = response.data.video;
        datashow_flag.value = true;
    }).catch((error:any)=>{
        ShowErrorMessage(error + " 服务器链接错误，即将跳转");
        // setTimeout(back,5000);
    });
}

const SiftUpdate = (ip_rq:string,gender_rq:string,date_rq:string,like_rq:string,reply_rq:string,emotion_rq:string)=>{
    pn.value = 1;
    ip.value = ip_rq;
    gender.value = gender_rq;
    date.value = date_rq;
    like.value = like_rq;
    reply.value = reply_rq;
    emotion.value = emotion_rq;
    console.log(gender.value)

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
    let flag = false;
    axios.get(url,{
        params:{
            bv:bv.value
        }
    }).then((org_response)=>{
        let response =org_response.data;
        chartdata.value[x] = response.data;
        if(x==0)chartshow0_flag.value = true;
        if(x==1)chartshow1_flag.value = true;
    }).catch((error)=>{
        ShowErrorMessage(error + " 获取统计图数据出错");
    })
}

onMounted(()=>{
    get_page_comment(bv.value,1,page_len,pn.value-1);//get the first page and total page
    GetChartData(overviewurl,0);
    GetChartData(ipAnalysurl,1);
    //get the overview data from backside
    //get all the ip analys data from backside
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
    font-size: 2vh;
    background-color: var(--color-tag);
    overflow: hidden;
}

#information{
    width: 100%;
    overflow: hidden;
}

#table{
    width: 100%;
}

.transition-animate{
    margin-top: 15vh;
    margin-top: 15vh;
    width: 100%;
}

.transition-animate .el-progress--line {
  margin-bottom: 15px;
  width: 300px;
}

.pagecount{
    margin-top: 40px;
    margin-bottom: 20px;
}
</style>