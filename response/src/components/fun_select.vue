<template>
    <div id="select-part" class=""> 
            <img src="/resource/picture/blueArch.png" alt="" :style="{boxShadow:`var(--el-box-shadow-dark)`}">
                 <el-select v-model="enter" effect="light" :popper-append-to-body="false" class="select-style">
                    <el-option value="selectA" id="seA" v-bind:label="fun1"></el-option>
                    <el-option value="selectB" id="seB" v-bind:label="fun2"></el-option>
                    <el-option value="selectC" id="seC" v-bind:label="fun3"></el-option>
                 </el-select>
    </div> 

    
</template>

<script>
export default{
    data() {
        return {
            fun1:"视频评论分析",
            fun2:"上传评论分析",
            fun3:"单个评论分析",
            enter:"selectA",
            select:0,
            url_ComAnaly:0,
            file_ComAnaly:1,
            single_ComAnaly:2
        }
    },
    methods:{
        Check(){
            switch(this.enter){
                case "selectA":
                    return this.url_ComAnaly;    
                case "selectA":
                    return this.file_ComAnaly;
                case "selectA":
                    return this.single_ComAnaly;
                default:
                    this.enter = "selectA";
                    return this.url_ComAnaly;
            }
        }
    },
    mounted() {
        this.select = this.Check();
        this.$emit("select",this.select);
    },
    watch:{
         enter(newValue){
            console.log(newValue);
           if(newValue == "selectA")this.$emit("select",this.url_ComAnaly);
           if(newValue == "selectB") this.$emit("select",this.file_ComAnaly);
           if(newValue == "selectC") this.$emit("select",this.single_ComAnaly);
        } 
    }
}
</script>

<style scoped>

.select-style {
    width: 25vh;
    margin-right: 0px;
    padding: 0px;
    position: absolute;
     top: 3vh; 
    right: inherit;
  }

.border{
    border: solid black 0.5px;
}

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
}
</style>