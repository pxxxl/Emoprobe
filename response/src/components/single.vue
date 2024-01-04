
<template>
        <div class="backimg"></div>
        <div id="input" class="center dis-flex center-flex">
            <!-- <span class="center select-no" style="margin-top: 5vh; font-size: 15px;">请输入单个评论进行评论分析</span> -->
            <el-input id="" v-model="comment" placeholder="请输入单个评论进行评论分析" class="center input-size" @keyup.enter="Update" size="large"></el-input>
            <el-button type="primary" @mouseleave="(event) => { event.target.blur() }"  @click="Update" :loading="loadin_flag" loading-icon="Eleme" class="commitbtn">{{ commitNotice }}</el-button>
            <Transition name="fade" mode="in-out">
                <div class="dis-flex center-flex notice" v-if="noticevisible">
                    内容不能为空
                </div>
            </Transition>
        </div>
    <div id="Responseshow" height="300px" v-if="result != null" style="background-color: white;" :style=" {boxShadow:`var(--el-box-shadow-dark)`}">
        <el-scrollbar>
            <el-table :data="result" style="width: 100%" :border="true">
                <el-table-column prop="key" label="序号" width="60" />
                <el-table-column prop="content" label="评论" width="210" />
                <el-table-column prop="emotion" label="情感分析" width="90" />
                <el-table-column prop="oprate_time" label="操作时间" width="240" />
            </el-table>
        </el-scrollbar>
    </div>
    <el-button type="primary" 
        @mouseleave="(event)=>{event.target.blur()}"  
        @click="Clear" 
        style="margin-left: 50%;margin-top: 2vh;transform: translateX(-50%);margin-bottom: 40px;"
        v-if="result != null"
    >
    清空列表
    </el-button>
</template>

<script>
import axios from 'axios';
import {ShowErrorMessage} from '@/assets/g.js'
import NothingShow from './NothingsShow.vue';

export default {
    data(){
        return{
            comment:"",
            commitNotice:"提交",
            api:"/api/v1/sentence",
            result:null,
            noticevisible:false,
            loadin_flag:false
        }
    },
    components:{
        NothingShow
    },
    methods: {
        Update(){
            if(this.loadin_flag == true)return;
            if(this.comment == null || this.comment ==""){
                this.noticevisible = true;
                setTimeout(()=>{
                    this.noticevisible = false;
                },1000);
                return;
            }
            this.loadin_flag = true;
            axios.post(this.api,JSON.stringify({
                comments:[this.comment]
            }),{
                headers:{
                   'content-type':'application/json'
                }
            }).then((org_response)=>{
                    let data =  org_response.data;
                    this.DataProccess(data);
            }).catch((error_msg)=>{
                ShowErrorMessage(error_msg);
            })
        },
        DataProccess(res){
            if(res.code == 409) {
                ShowErrorMessage("感知失败");
                this.loadin_flag = false;
                return;
            }
            if(this.result == null)this.result = new Array();
            let key = this.result.length + 1;
            this.result.push({
                key:key,
                oprate_time:res.data.operation_time,
                content:res.data.comments[0].content,
                emotion:res.data.comments[0].emotion
            });
            this.comment = "";
            console.log(this.result);
            this.loadin_flag = false;
        },
        Clear(){
            this.result = null;
        }
    },
    mounted() {
    },
}
</script>

<style scoped>
.commitbtn{
    margin-top: 5px;
}
.backimg{
    width: 60%;
    height: 200px;
    margin: auto;
    background-image: url('/resource/picture/blueArch.png');
    background-repeat: no-repeat;
    background-size: 100% 100%;
    margin-top: 1vh;
}
#Responseshow{
    height: 300px;
    width: 600px;
    margin: auto;
    margin-top: 5vh;
}
#input{
    display: flex;
    flex-direction: column;
    height: 160px;
    width: 60%;
    backdrop-filter: blur(6px);
    border-radius: 10px;
}
.center{
    margin: auto;
}

.input-size{
    width:45%;
    margin-top: 10px;
    margin-bottom: 10px;
}

.notice{
    background-color: black;
    color: white;
    margin-top: 3vh;
    width: 100px;
    height: 40px;
    border-radius: 10px;
    transition: all 1s;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.8s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
