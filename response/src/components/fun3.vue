
<template>
    <div>
        <span>功能3：输入单个评论进行评论分析</span>
        <el-input v-model="comment" placeholder="Please Input"></el-input>
        <el-button type="primary" @mouseleave="(event)=>{event.target.blur()}"  @click="Update">{{commitNotice}}</el-button>
    </div>
</template>

<script>
import axios from 'axios';
import {getInterFace} from '@/assets/g.js'
export default {
    data(){
        return{
            comment:null,
            commitNotice:"提交",
            api:null
        }
    },
    methods: {
        Update(){
            this.api = getInterFace();
            axios.post(this.api,this.comment).then((response)=>{
                   
                    //TODO
            }).catch((error_msg)=>{

            })
        }
    },
    mounted() {
        this.api = getInterFace(3);
    },
}
</script>

<style scoped>

</style>
