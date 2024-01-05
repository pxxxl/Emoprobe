<template>
    <el-dialog  class="dis-flex direction-column-flex align-items-center border" v-model="dialogVisiable" title="文件上传评论分析">
            <div class="dis-flex direction-column-flex ">
                <el-upload
                    v-model:file-list = "filelist"
                    class="dis-flex center-flex upload"
                    :action = "api"
                    :show-file-list="false"
                    ref= "uploadRef"
                    :auto-upload = "false"
                    :limit = "1"
                    accept = ".json"
                    :on-exceed="handleExceed"
                    :on-change="handelChange"
                    :on-error="handleError"
                    :on-success = "handleSuccess"
                    >
                    <el-button 
                        type="primary" 
                        native="button" 
                        class="button center" 
                        @mouseleave="(event) => event.target.blur()" 
                    >
                       选择文件
                    </el-button> 
                </el-upload>

                <div v-if="filelist.length == 0" class="notice dis-flex center-flex select-no" style="font-size: larger;">
                    请选择文件
                </div>

                <div v-if="filelist.length > 0" class="notice margin-auto">
                    <upload-item v-for="file in filelist" 
                        :file="file" 
                        :key="file.uid" 
                        class="dis-flex direction-row-flex center-flex item margin-auto"
                    >  
                        <el-icon class="set-interval"><Document /></el-icon>
                        <div class="name">{{ file.name }}</div>
                        <el-icon class="icon dis-flex center-flex"><Delete @click="Delete" class="pointer bigger"/></el-icon>
                    </upload-item>
                </div>

                <div class="dis-flex direction-row-flex">
                    <el-button  class="button center"  type="primary" @click="submit"  @mouseleave="(event) => event.target.blur()" :disabled="filelist.length == 0" :loading="load_flag">
                        提交
                    </el-button>
                    <el-button  class="button center"  type="primary" @click="dialogVisiable=false"  @mouseleave="(event) => event.target.blur()" >
                        取消
                    </el-button>
                </div>
            </div>

        </el-dialog>
</template>

<script>
import axios from 'axios'
import {translateBV,ShowErrorMessage} from '@/assets/g.js'
export default{
    props:['visiable'],
    data() {
        return {
            filelist:[],
            uploadRef:null,
            api:'/api/v1/comments',
            dialogVisiable:false,
            load_flag:false
        }
    },
    methods:{
        Delete(){
            this.filelist = [];
        },
        handleExceed(file,oldfilelist){
            let isJSON = (file[0].type == 'application/json');
            if(isJSON)this.filelist[0] = file[0];
            else{
              ShowErrorMessage("请上传json格式的文件");
            }
        },
        handelChange(uploadFile,uploadFiles){
            let isJson = (uploadFile.raw.type ==  'application/json');
            if(!isJson){
                ShowErrorMessage("请上传json格式的文件")
                this.filelist = [];
            }
        },
        handleError(error, uploadFile, uploadFiles){//back up
            ShowErrorMessage("Fail connect : "+error);
        },  
        handleSuccess(org_response,file,files){//back up
            console.log(org_response);
        },
        submit(){
            if(this.filelist == 0){
                ShowErrorMessage('请选择文件');
                return;
            }
            this.load_flag = true;
            let fileread = new FileReader();
            fileread.onload = ()=>{
                axios.post(this.api,fileread.result,{
                    headers:{
                        'content-type':'application/json'
                    }
                }).then((org_repsone)=>{
                    let response = org_repsone.data;
                    if(response.code == 409 || response.code == 500){
                        ShowErrorMessage("感知错误");
                        return;
                    }
                    console.log(response);
                    let bv_num = response.data.video.video_bid;
                    this.load_flag = false;
                    this.$router.push({
                        path:"/datashow",
                        query:{bv:bv_num}
                    });
                }).catch((error)=>{
                    ShowErrorMessage(error);
                    this.load_flag = false;
                })
            }
            let filestring = fileread.readAsText(this.filelist[0].raw);
            // this.uploadRef.submit();
        }
    },
    mounted() {
        this.uploadRef = this.$refs.uploadRef;
    },
    watch:{
        visiable(){
            this.dialogVisiable = true;
        }
    }
}



</script>

<style scoped>
.notice{
    width: 100%;
    height: 100px;
}
.center{
    margin: auto;
}

.button{
    margin-top: 1vh;
    margin-right: 1vh;
    margin-left: 1vh;
    margin-bottom: 1vh;
}
.bigger{
    scale: 1.2;
}
.item{
    width: 50%;
}
.set-interval{
    margin-right: 1vh;
    flex: 1;
}
.name{
    font-size: large;
    margin-right:  1vh;
    margin-left: 2vh;
    flex: 7;
}
.icon{
    flex: 1;
}
.scale{
    scale: 1.3;
}
.upload{
    margin-bottom: 10px;
    margin-top: 10px;
}

</style>