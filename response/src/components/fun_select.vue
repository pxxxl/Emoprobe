<template>
    <div id="select-part" class="dis-flex direction-row-flex" :style=" {boxShadow:`var(--el-box-shadow-light)`}"> 
            <div class="pic-container">
                <img src="/resource/picture/blueArch.png" style="display: block;width: 100%;height: 100%;">
            </div>
            <div class="container dis-flex direction-row-flex align-items-center">
                    <button v-bind:class="button_1_class " @mouseleave="(event)=>event.target.blur()" :value="vedio_ComAnaly" @click="TargetChange(vedio_ComAnaly)" v-if="bs">{{vedio_analys_notice}}</button>
                    <button v-bind:class="button_2_class" @mouseleave="(event)=>event.target.blur()" :value="single_ComAnaly" @click="TargetChange(single_ComAnaly)" v-if="bs">{{single_analys_notice}}</button>
                    <button v-bind:class="button_3_class " @mouseleave="(event)=>event.target.blur()" :value="file_ComAnaly" @click="TargetChange(file_ComAnaly)" v-if="bs">{{file_analys_notice}}</button>
            </div>
    </div> 
</template>

<script>
export default{
    data() {
        return {
            vedio_analys_notice:"视频评论分析",
            single_analys_notice:"快速评论感知",
            file_analys_notice:"上传文件分析",
            select:1,
            vedio_ComAnaly:1,
            single_ComAnaly:2,
            file_ComAnaly:3,
            button_1_class:null,
            button_2_class:null,
            button_3_class:null
        }
    },
    methods:{
        Check(){
        },
        TargetChange(num){
            if(num == 1){
                this.button_1_class = ['button-act'];
                this.button_2_class = ['button'];
                this.button_3_class = ['button'];
            }
            else if(num==2){
                this.button_2_class = ['button-act'];
                this.button_1_class = ['button'];
                this.button_3_class = ['button'];
            }
            else{
                this.button_3_class = ['button-act'];
                this.button_1_class = ['button'];
                this.button_2_class = ['button'];
            }
            this.select = num;
            this.$emit("select",this.select);
        }
    },
    props:['bs'],
    mounted() {
        this.button_1_class = ['button-act'];
        this.button_2_class = ['button'];
        this.button_3_class = ['button'];
    },
    watch:{
    }
}
</script>

<style scoped>
#select-part{
    height: 70px;
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