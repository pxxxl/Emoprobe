<template>
    <div id="fun1">
        <form id="form1" class="center">
            <span id="notice" class="center">{{ url_notice }}</span> 
            <el-input v-model.lazy="video" :autofocus="true" :clearable="true" class="input-size center" placeholder="Please Input" :style="{boxShadow:`var(--el-box-shadow-dark)`}"/>
            <el-button type="primary" native="button" class="button center" @mouseleave="(event)=>event.target.blur()" @click="Postdata">{{ commitNotice }}</el-button>
        </form>
        <func1Chart v-bind:comment_arr = "com" v-bind:chart_data = "show" v-if="success"/>
        <img src="" alt="">
    </div>
</template>

<script>
import func1Chart from './func1Chart.vue'//import the component
import axios from 'axios'
import {getInterFace,translateBV,ShowErrorMessage} from '@/assets/g.js'

export default{
    data() {
        return {
            url_notice:"请输入分析对象视频的url",
            video:"",
            commitNotice:"提交",
            com:null,
            show:null,
            success:false,
            api:null
        }
    },
    components:{
        func1Chart
    },
    props:["op1"],
    methods: {
        Postdata(){
            alert("啥都没有！");
            let postdata = this.video;
            if(postdata.video[0] != 'B' || postdata.video[1] != 'V')
                postdata.video = translateBV(postdata.video);
            axios.post(this.api,JSON.stringify(postdata))
            .then(function (response){
                let result = JSON.parse(response);
                if(result == null){
                    console.log(console.error());
                    alert("接收数据错误");
                }
                this.com = result.data;
                //TODO
            }).catch((error) => {
                ShowErrorMessage("error:posting data" + error);
            });
        }
    },
    mounted() {
        this.api = getInterFace(1);
    },
}
</script>

<style scoped>
.input-size{
    width: 40%;
    border-radius: 4px;
    border: 1px solid rgba(0, 0, 255,0.3);
}

#form1{
    display: flex;
    flex-flow: column;
    width: 50%;
    margin: auto;
    padding: 0px;
}

.button{
    width: 12vh;
    margin-top: 2vh!important;
}

#notice{
    font-size: large;
    user-select: none;
    margin-bottom: 2vh;
    margin-top: 5vh;
}

.center{
    margin: auto;
}
</style>