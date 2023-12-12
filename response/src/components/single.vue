
<template>
    <div id="input" class="center">
        <span class="center select-no" style="margin-top: 5vh; font-size: 4;">请输入单个评论进行评论分析</span>
        <el-input id="input" v-model="comment[0]" placeholder="Please Input" class="center input-size" @keyup.enter="Update"></el-input>
        <el-button type="primary" @mouseleave="(event)=>{event.target.blur()}"  @click="Update" class="center">{{commitNotice}}</el-button>
        <Transition name="fade" mode="in-out">
            <div class="dis-flex center-flex notice" v-if="noticevisible">
                内容不能为空
            </div>
        </Transition>
    </div>
    <div id="Responseshow" v-if="result != null">
        <table>
            <tr>
                <th>评论内容</th>
                <th>情感</th>
            </tr>
            <tr v-for="item in result.comments">
                <td>{{ item.content }}</td>
                <td>{{ item.emotion }}</td>
            </tr>
        </table>
    
    </div>
</template>

<script>
import axios from 'axios';
import {ShowErrorMessage} from '@/assets/g.js'
import NothingShow from './NothingsShow.vue';

export default {
    data(){
        return{
            comment:new Array(1),
            commitNotice:"提交",
            api:"/api/v1/sentence",
            result:null,
            noticevisible:false,
            input:null
        }
    },
    components:{
        NothingShow
    },
    methods: {
        Update(){
            if(this.comment[0] == null){
                this.noticevisible = true;
                setTimeout(()=>{
                    this.noticevisible = false;
                },1000);
                return;
            }
            axios.post(this.api,this.comment).then((response)=>{
                    let org =  response.data;
                    this.DataProccess(org);
            }).catch((error_msg)=>{
                ShowErrorMessage(error_msg);
            })
        },
        DataProccess(org_data){
            if(org_data.code === 200) {
                ShowErrorMessage("感知失败");
                return;
            }
            this.result =org_data.data;
        }
    },
    mounted() {
        this.input = document.getElementById('input');
    },
}
</script>

<style scoped>
#input{
    display: flex;
    flex-direction: column;
    width: 50%;
    margin: auto;
}
.center{
    margin: auto;
}

.input-size{
    width: 40%;
    margin-top: 5vh;
    margin-bottom: 3vh;
}

.notice{
    background-color: black;
    color: white;
    margin-top: 3vh;
    width: 100px;
    height: 40px;
    margin-left: 50%;
    border-radius: 10px;
    transform: translateX(-50%);
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
