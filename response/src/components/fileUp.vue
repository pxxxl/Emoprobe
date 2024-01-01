<template>
    <div  class="dis-flex direction-column-flex align-items-center">
            <span id="notice">
                文件上传评论分析
            </span>
            <div class="dis-flex direction-row-flex ">
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
                        <el-icon><FolderOpened class="scale"/></el-icon>
                    </el-button> 
                </el-upload>

                <el-button  class="button center"  type="primary" @click="submit">
                    <el-icon><Upload class="scale"/></el-icon>
                </el-button>
            </div>

            <div v-if="filelist.length > 0" class="fl margin-auto">
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
        </div>
</template>

<script>
import axios from 'axios'
import {translateBV,ShowErrorMessage} from '@/assets/g.js'
export default{
    data() {
        return {
            filelist:[],
            uploadRef:null,
            api:'/api/v1/comments'
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
            let fileread = new FileReader();
            fileread.onload = ()=>{
                // console.log(fileread.result);
                axios.post(this.api,fileread.result,{
                    headers:{
                        ' content-type':'application/json'
                    }
                }).then((org_repsone)=>{
                    let response = org_repsone.data;
                    if(response.code == 409){
                        ShowErrorMessage("感知错误");
                        this.filelist = [];
                        return;
                    }
                    console.log(response);
                    let bv_num = response.data.video.video_bid;
                    this.$router.push({
                        path:"/datashow",
                        query:{bv:bv_num}
                    });
                })
            }
            let filestring = fileread.readAsText(this.filelist[0].raw);
            // this.uploadRef.submit();
        }
    },
    mounted() {
        this.uploadRef = this.$refs.uploadRef;
    },
}



</script>

<style scoped>
#notice{
    font-size: 16px;
    user-select: none;
    margin-bottom: 2vh;
    margin-top: 5vh;
}
.center{
    margin: auto;
}

.button{
    width: 5vh;
    margin-left: 0px!important;
    margin-right: 2vh!important;
}
.fl{
    position: relative;
    top: 5vh;
    width: 60%;
    min-height: 5vh;
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
    flex: 7;
}
.icon{
    flex: 1;
}
.scale{
    scale: 1.3;
}

</style>