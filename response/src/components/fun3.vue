
<template>
    <div id="input" class="center">
        <span class="center select-no">功能3：输入单个评论进行评论分析</span>
        <el-input v-model="comment" placeholder="Please Input" class="center input-size"></el-input>
        <el-button type="primary" @mouseleave="(event)=>{event.target.blur()}"  @click="Update" class="center">{{commitNotice}}</el-button>
    </div>
    <NothingShow />
</template>

<script>
import axios from 'axios';
import {getInterFace} from '@/assets/g.js'
import NothingShow from './NothingsShow.vue';

export default {
    data(){
        return{
            comment:null,
            commitNotice:"提交",
            api:null
        }
    },
    components:{
        NothingShow
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
}
</style>
