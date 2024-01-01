<template>
    <el-scrollbar class="list border">
        <p class="select-no dis-flex center-flex" style="font-size: 16px;"><b>数据库视频列表</b></p>
        <router-link class="none-decoration link" v-for="bv_inform in videolist" :to="{path:'/datashow',query:{bv:bv_inform.video_bid}}" ><b>{{ titleProccess(bv_inform) }}</b></router-link>
    </el-scrollbar>
</template>

<script>
import axios from 'axios';
import { List } from 'echarts';
import {ShowErrorMessage} from '@/assets/g.js'

export default{
    data() {
        return {
            videolist:null,
        }
    },
    mounted(){
        axios.get('/api/v1/videos/list')
        .then((org_response)=>{
            let response = org_response.data;
            if(response == null){
                ShowErrorMessage("接收数据错误");
                return;
            }
            switch(response.code){
                case 409:
                    ShowErrorMessage("请求失败");
                    break;
                case 200:
                    this.videolist = response.data.videos;
                    break;
            }
        }).catch((error)=>{
            ShowErrorMessage(error+"连接错误");
        })
    },
    methods:{
        titleProccess(video){
            if(video.video_title.length > 20)
            {
                return video.video_title.slice(0,20) + "...";
            }
            else return video.video_title;
        }
    }
}
</script>

<style scoped>
.link{
    padding-top: 1vh;
    padding-bottom: 1vh;
    padding-left: 5px;
    padding-right: 4px;
    font-size: 13px;
    width: 100%;
    color: var( --color-font-black);
    display: flex;
}
.link:hover{
    color:  var(--color-font-link);
}
.list{
    height: 83vh;
    border-radius: 3vh;
    backdrop-filter:blur(6px);
    color: var( --color-font-black);
}
</style>