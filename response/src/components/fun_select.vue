<template>
    <div id="select-part" class=""> 
            <img src="/resource/picture/blueArch.png" alt="" :style="{boxShadow:`var(--el-box-shadow-dark)`}">
            <div class="container dis-flex direction-row-flex center-flex">
                <el-button class="button border" @mouseleave="(event)=>event.target.blur()" :value="vedio_ComAnaly" @click="TargetChange(vedio_ComAnaly)">{{vedio_analys}}</el-button>
                <el-button class="button border" @mouseleave="(event)=>event.target.blur()" :value="single_ComAnaly" @click="TargetChange(single_ComAnaly)">{{single_analys}}</el-button>
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
    mounted() {
    },
    watch:{
    }
}
</script>

<style scoped>
#select-part{
    height: 10vh;
    width: 100%;
    top: 0;
    right: 5%;
    background-color: var(--color-head);
}

img{
    height: 100%;
    width: 20%;
    margin: 0px;
    float: left;
}

.button{
   flex: 1;
   height: 80%!important;
}

.container{
    top: 0px;
    margin: auto;
    height: 10vh;
    width: 20vh;
}
</style>