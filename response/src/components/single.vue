
<template>
    <div id="input" class="center">
        <span class="center select-no">功能3：输入单个评论进行评论分析</span>
        <el-input v-model="comment[0]" placeholder="Please Input" class="center input-size"></el-input>
        <el-button type="primary" @mouseleave="(event)=>{event.target.blur()}"  @click="Update" class="center">{{commitNotice}}</el-button>
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
            api:"null",
            result:null
        }
    },
    components:{
        NothingShow
    },
    methods: {
        Update(){
            this.api = getInterFace();
            axios.post(this.api,this.comment).then((response)=>{
                    let org =  JSON.parse(response);
                    this.DataProccess(org);
            }).catch((error_msg)=>{

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
</style>
