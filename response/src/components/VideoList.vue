<template>
    <div class="dis-flex direction-column-flex align-items-center list border">
        <p class="select-no" style="font-size: 16px;"><b>数据库视频列表</b></p>
        <router-link class="none-decoration link dis-flex center-flex" v-for="bv_inform in videolist" :to="{path:'/datashow',query:{bv:bv_inform.video_bid}}" ><b>{{ titleProccess(bv_inform) }}</b></router-link>
    </div>
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
    margin-top: 1.2vh;
    margin-bottom: 1.2vh;
    margin-left: 4px;
    margin-right: 4px;
    font-size: 13px;
    text-align: center;
    color: var( --color-font-black);
}
.link:hover{
    color:  var(--color-font-link);
}
.list{
    border-radius: 3vh;
    backdrop-filter:blur(6px);
    color: var( --color-font-black);
}
</style>