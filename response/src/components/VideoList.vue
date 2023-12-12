<template>
    <div class="dis-flex direction-column-flex align-items-center">
        <h3 class="select-no">数据库视频列表</h3>
        <router-link class="none-decoration link dis-flex center-flex" v-for="bv_inform in videolist" :to="{path:'/datashow',query:{bv:bv_inform.video_bid}}" >{{ titleProccess(bv_inform) }}</router-link>
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
            if(video.video_title.length > 22)
            {
                return video.video_title.slice(0,22) + "...";
            }
            else return video.video_title;
        }
    }
}
</script>

<style scoped>
.link{
    margin-top: 1vh;
    margin-bottom: 1vh;
    font-size: 1.8vh;
}
</style>