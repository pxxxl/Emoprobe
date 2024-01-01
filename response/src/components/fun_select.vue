<template>
    <div id="select-part" class="dis-flex direction-row-flex" :style=" {boxShadow:`var(--el-box-shadow-light)`}"> 
            <div class="pic-container">
                <img src="/resource/picture/blueArch.png" style="display: block;width: 100%;height: 100%;">
            </div>

            <div class="container dis-flex direction-row-flex align-items-center">
                <button v-bind:class="button_1_class " @mouseleave="(event)=>event.target.blur()" :value="vedio_ComAnaly" @click="TargetChange(vedio_ComAnaly)" v-if="bs">{{vedio_analys}}</button>
                <button v-bind:class="button_2_class" @mouseleave="(event)=>event.target.blur()" :value="single_ComAnaly" @click="TargetChange(single_ComAnaly)" v-if="bs">{{single_analys}}</button>
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
            single_ComAnaly:2,
            button_1_class:null,
            button_2_class:null
        }
    },
    methods:{
        Check(){
        },
        TargetChange(num){
            if(num == 1){
                this.button_1_class = ['button-act'];
                this.button_2_class = ['button'];
            }
            else{
                this.button_2_class = ['button-act'];
                this.button_1_class = ['button'];
            }
            this.select = num;
            this.$emit("select",this.select);
        }
    },
    props:['bs'],
    mounted() {
        this.button_1_class = ['button-act'];
        this.button_2_class = ['button'];
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
   font-size: 15px;
   height: 50%;
   width: 10%;
   margin-left: 2px;
   margin-right: 2px;
   background-color: var( --color-button-nohover);
   color: black;
   border: 0px;
}
.button:hover{
    background-color: var(--color-button-hover);
}

.button-act{
    font-size: 15px;
   height: 50%;
   width: 10%;
   margin-left: 2px;
   margin-right: 2px;
   background-color: var( --color-button-act);
   color: black;
   border: 0px;
}

.container{
    flex: 8;
}

.pic-container{
    flex: 2;
}
</style>