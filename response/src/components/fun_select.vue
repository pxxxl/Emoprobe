<template>
    <div id="select-part" class="dis-flex direction-row-flex" :style=" {boxShadow:`var(--el-box-shadow-light)`}"> 
            <div class="pic-container">
                <img src="/resource/picture/blueArch.png" style="display: block;width: 100%;height: 100%;">
            </div>

            <div class="container dis-flex direction-row-flex align-items-center">
                <el-button class="button " @mouseleave="(event)=>event.target.blur()" :value="vedio_ComAnaly" @click="TargetChange(vedio_ComAnaly)" v-if="bs">{{vedio_analys}}</el-button>
                <el-button class="button " @mouseleave="(event)=>event.target.blur()" @mousehover="" :value="single_ComAnaly" @click="TargetChange(single_ComAnaly)" v-if="bs">{{single_analys}}</el-button>
            </div>
    </div> 
</template>

<script>
export default{
    data() {
        return {
            vedio_analys:"视频评论分析",
            single_analys:"快速评论感知",
            select:1,
            vedio_ComAnaly:1,
            single_ComAnaly:2
        }
    },
    methods:{
        Check(){
        },
        TargetChange(num){
            this.select = num;
            this.$emit("select",this.select);
        }
    },
    props:['bs'],
    mounted() {
    },
    watch:{
    }
}
</script>

<style scoped>
#select-part{
    height: 12vh;
    width: 100%;
    top: 0;
    right: 5%;
    background-color: var(--color-head);
}

.button{
   height: 50%;
   width: 10%;
   background-color: var( --color-button-nohover);
   color: black;
   border: 0px;
}
.button:hover{
    background-color: var(--color-button-hover);
}

.container{
    flex: 8;
}

.pic-container{
    flex: 2;
}
</style>