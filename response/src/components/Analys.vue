<template>
    <Fun_select :bs="false" @back="back" />
    <el-button id="backpart" @click="back">
        <el-icon>
            <ArrowLeftBold />
        </el-icon>
        返回
    </el-button>
    <div class="main">
        <div id="information-nav" v-show="datashow_flag" class="dis-flex direction-row-flex">
            <el-descriptions title="视频信息" direction="horizontal" :border="true" :column="1" class="inforlist">
                <el-descriptions-item label="视频BV号" min-width="120">{{ video_information.video_bid }}</el-descriptions-item>
                <el-descriptions-item label="视频标题">{{ video_information.video_title }}</el-descriptions-item>
                <el-descriptions-item label="最后操作时间">{{ video_information.operation_time }}</el-descriptions-item>
                <el-descriptions-item label="UP主用户名">{{ video_information.owner_name }}</el-descriptions-item>
                <el-descriptions-item label="视频分区">{{ video_information.video_tables }}</el-descriptions-item>
                <el-descriptions-item label="发布时间">{{ video_information.video_pubdate }}</el-descriptions-item>
                <el-descriptions-item label="点赞数">{{ video_information.video_like }}</el-descriptions-item>
                <el-descriptions-item label="投币数">{{ video_information.video_coin }}</el-descriptions-item>
                <el-descriptions-item label="收藏数">{{ video_information.video_favorite }}</el-descriptions-item>
                <el-descriptions-item label="分享数">{{ video_information.video_share }}</el-descriptions-item>
                <el-descriptions-item label="评论数">{{ video_information.video_reply }}</el-descriptions-item>
                <el-descriptions-item class="inshow border" label="视频简介">{{ video_information.video_desc
                }}</el-descriptions-item>
            </el-descriptions>
        </div>
        <h1 class="dis-flex center-flex" style="margin-top: 50px;">评论统计结果</h1>
        <el-radio-group v-model="show" style="margin-left: 50px;margin-bottom: 20px;">
            <el-radio :label="1" size="large">评论中国Ip分布</el-radio>
            <el-radio :label="2" size="large">Ip占比</el-radio>
            <el-radio :label="3" size="large">各情感的Ip占比</el-radio>
            <el-radio :label="4" size="large">各Ip的情感占比</el-radio>
            <el-radio :label="5" size="large">情感分类的人数</el-radio>
            <el-radio :label="6" size="large">分析结果列表一览</el-radio>
        </el-radio-group>
        <!-- <el-divider border-style="double" /> -->
        <div id="charts" v-show="show != 6">
            <div v-loading="!(chartshow0_flag && chartshow1_flag)" style="height: 200px;width: 100%;"
                v-if="!(chartshow0_flag && chartshow1_flag)"></div>
            <chart :overview="chartdata[0]" :ipAnalys="chartdata[1]" v-if="chartshow0_flag && chartshow1_flag"
                :showpart="show" />
        </div>
        <el-divider border-style="double" />

        <div id="table" v-show="show == 6">
            <div class="pagination-block">
                <sift @sift="SiftUpdate" v-if="datashow_flag && chartshow0_flag && chartshow1_flag" :ipArr="ipArr" />
                <div class="demonstration">
                    <div class="dis-flex center-flex pagecount">
                        <el-pagination layout="prev, pager, next" style="width: 50vh;" :hide-on-single-page="true"
                            :page-size="page_len" v-model:page-count="all_pagenum" v-model:current-page="pn"
                            background="blue" />
                    </div>
                    <div v-loading="!datashow_flag" style="height: 200px;width: 100%;" v-if="!datashow_flag"></div>
                    <el-table :data="per_pageCom" style="width: 100%;" v-if="datashow_flag" :border="true">
                        <el-table-column prop="user_uid" label="用户id" align="center" min-width="100"></el-table-column>
                        <el-table-column prop="user_name" label="用户名称" align="center"></el-table-column>
                        <el-table-column prop="user_ip" label="用户IP" align="center"></el-table-column>
                        <el-table-column prop="user_sex" label="性别" align="center"></el-table-column>
                        <el-table-column prop="comment_date" label="日期" align="center" min-width="150"></el-table-column>
                        <el-table-column prop="comment_text" label="评论文本" align="center" min-width="400"></el-table-column>
                        <el-table-column prop="comment_like" label="点赞数" align="center"></el-table-column>
                        <el-table-column prop="comment_reply" label="回复数" align="center"></el-table-column>
                        <el-table-column prop="emotion" label="情感" align="center"></el-table-column>
                    </el-table>
                </div>
            </div>
        </div>
    </div>
    <Backtop />
</template>

<script lang="ts" setup>
import { Ref, nextTick, onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router'
import axios, { formToJSON } from 'axios';
import { ShowErrorMessage } from '@/assets/g.js';
import sift from './sift.vue';
import chart from './chart.vue';
import { Loading } from 'element-plus/es/components/loading/src/service';
import Backtop from './backtop.vue';
import Fun_select from './fun_select.vue';


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
const pn = ref(1);

const show = ref(1);
if (route.query.bv != null) bv.value = route.query.bv.toString();
video_information.value = {
    video_bid: null,
    video_title: null,
    operation_time: null,
    owner_name: null,
    video_tables: null,
    video_pubdate: null,
    video_like: null,
    video_coin: null,
    video_favorite: null,
    video_share: null,
    video_reply: null,//11
    video_desc: null
}

const chartshow0_flag = ref(false);
const chartshow1_flag = ref(false);
const datashow_flag = ref(false);

const ip = ref("");
const gender = ref("");
const date = ref("");
const like = ref("");
const reply = ref("");
const emotion = ref("");

const chartdata = ref([null, null]);
const ipArr = ref();

interface Params {
    bv: string,
    autopost: number,
    n_per_page: number,
    pn: number,
    user_ip: string,
    user_sex: string,
    comment_date: string,
    comment_like: string,
    comment_reply: string,
    emotion: string
}

const back = () => {
    router.push({
        path: "/"
    });
}

const get_page_comment = (bvString: string, autopost: number, pageLen: number, page: number, ip_sift?: string, sex_sift?: string, date_sift?: string, like_sift?: string, reply_sift?: string, emotion_sift?: string) => {
    let params: Params = {} as Params;
    params.bv = bvString;
    params.autopost = autopost;
    params.n_per_page = pageLen;
    params.pn = page;

    if (ip_sift && ip_sift != "") params.user_ip = ip_sift;
    if (sex_sift && sex_sift != "") params.user_sex = sex_sift;
    if (date_sift && date_sift != "") params.comment_date = date_sift;
    if (like_sift && like_sift != "") params.comment_like = like_sift;
    if (reply_sift && reply_sift != "") params.comment_reply = reply_sift;
    if (emotion_sift && emotion_sift != "") params.emotion = emotion_sift;

    axios.get(api, {
        params: params
    }).then((org_response: any) => {
        let response: any = org_response.data;
        if (response.code == 408 || !response) {
            ShowErrorMessage(response.msg + " 即将跳转");
            setTimeout(back, 5000);
        }
        all_pagenum.value = response.data.total_page_num;
        per_pageCom.value = response.data.comments;
        video_information.value = response.data.video;
        datashow_flag.value = true;
        GetChartData(overviewurl, 0);
        GetChartData(ipAnalysurl, 1);
    }).catch((error: any) => {
        ShowErrorMessage(error + " 服务器链接错误，即将跳转");
        setTimeout(back, 5000);
    });
}

const SiftUpdate = (ip_rq: string, gender_rq: string, date_rq: string, like_rq: string, reply_rq: string, emotion_rq: string) => {
    pn.value = 1;
    ip.value = ip_rq;
    gender.value = gender_rq;
    date.value = date_rq;
    like.value = like_rq;
    reply.value = reply_rq;
    emotion.value = emotion_rq;
    console.log(date.value)

    get_page_comment(bv.value, 1,
        page_len,
        pn.value - 1,
        ip.value,
        gender.value,
        date.value,
        like.value,
        reply.value,
        emotion.value
    );
}

const GetChartData = (url: string, x: number) => {
    let flag = false;
    axios.get(url, {
        params: {
            bv: bv.value
        }
    }).then((org_response) => {
        let response = org_response.data;
        chartdata.value[x] = response.data;
        if (x == 0 && response.data != null) chartshow0_flag.value = true;
        if (x == 1 && response.data != null && chartdata.value[1] != null) {
            chartshow1_flag.value = true;
            ipArr.value = chartdata.value[1].ip;
        }
    }).catch((error) => {
        ShowErrorMessage(error + " 获取统计图数据出错");
    })
}

const TurnToEleView = (id: string) => {
    document.getElementById(id)?.scrollIntoView({
        behavior: 'smooth',
        inline: 'end'
    });
}

onMounted(() => {
    get_page_comment(bv.value, 1, page_len, pn.value - 1);//get the first page and total page
});

watch(pn, (New_pn) => {
    get_page_comment(bv.value,
        1,
        page_len,
        pn.value - 1,
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
h1 {
    margin-bottom: 5vh;
}

#backpart {
    margin-bottom: 3vh;
}

.inforlist {
    width: 70%;
}

#nav {
    width: 30%;
    padding-top: 5%;
}

.nav-list {
    width: 30%;
    height: auto;
    list-style-type: none;
    padding: 0px;
    color: black;
}

li:hover {
    color: var(--color-font-linkE);
}

.turnto-size {
    font-size: 14px;
}

.main {
    margin-left: 30px;
    margin-right: 30px;
}

.inshow {
    padding: 1vh;
    font-size: 2vh;
}

#information-nav {
    width: 100%;
    height: auto;
}

#table {
    width: 100%;
    margin-bottom: 5vh;
}

.transition-animate {
    margin-top: 15vh;
    margin-top: 15vh;
    width: 100%;
}

.transition-animate .el-progress--line {
    margin-bottom: 15px;
    width: 300px;
}

.pagecount {
    margin-top: 40px;
    margin-bottom: 20px;
}</style>