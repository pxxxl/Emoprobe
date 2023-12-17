<template>
    <div  class="dis-flex direction-row-flex">
        <form id="form1">
            <span id="notice" class="center">{{ url_notice }}</span> 
            <div class="dis-flex direction-row-flex center-flex">
                <el-input 
                    v-model.lazy="video" 
                    type="textarea"
                    :show-word-limit="true"
                    :autosize="{ minRows: 3, maxRows: 5 }"
                    :autofocus="true" 
                    :clearable="true" 
                    class="input-size" 
                    placeholder="Please Input" 
                    :style="{boxShadow:`var(--el-box-shadow-dark)`}"
                    />

                <el-button 
                    type="primary" 
                    native="button" 
                    class="button center" 
                    @mouseleave="(event)=>event.target.blur()" 
                    @click="Postdata">
                    <el-icon><Plus class="scale"/></el-icon>
                </el-button>

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
                        @mouseleave="(event)=>event.target.blur()" 
                        >
                        <el-icon><FolderOpened class="scale"/></el-icon>
                    </el-button> 
                </el-upload>
                
                <el-button 
                    type="primary" 
                    native="button" 
                    class="button center" 
                    @mouseleave="(event)=>event.target.blur()" 
                    @click="getFile">
                    <el-icon><Download /></el-icon>
                </el-button>

            </div>
        </form>
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

</template>

<script>
import axios from 'axios'
import {translateBV,ShowErrorMessage} from '@/assets/g.js'
import NothingShow from './NothingsShow.vue'

export default{
    data() {
        return {
            url_notice:"请输入分析对象视频的url或上传json文件",
            video:"",
            commitNotice:"提交",
            com:null,
            show:null,
            success:false,
            filelist:[],
            uploadRef:null,
            api:'/api/v1/comments'
        }
    },
    components:{
        NothingShow
    },
    methods: {
        getFile(){
            let bv_str = "";
            console.log("下载");
            bv_str = translateBV(this.video);
            if(bv_str == "error"){
                ShowErrorMessage("提取bv号出现错误");
                return;
            }
            axios.get("/api/v1/crawl",{
                params:{
                    bv:bv_str
                }
            }).then((org_response)=>{
                let response = org_response.data;
                if(response.code == 407){
                    ShowErrorMessage("爬取信息失败");
                    return;
                }
                const a = document.createElement('a');
                a.download = "数据结果"+ bv_str +".json";
                a.style.display = 'none';
                const blob = new Blob([JSON.stringify(response.data)]);
                a.href = URL.createObjectURL(blob);
                a.click();
                document.body.removeChild(a);
                this.video = "";
            })
        },
        Postdata(){
            let bv_number = "";
            if(this.filelist.length > 0){
                this.submit();
            }
            else{//bv number post
                bv_number = translateBV(this.video);
               if(bv_number === "error"){
                    ShowErrorMessage("提取bv号出现错误");
                    return;
               }
               this.$router.push({
                    path:"/datashow",
                    query:{bv:bv_number}
               });
            }
        },
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
        handleError(error, uploadFile, uploadFiles){
            ShowErrorMessage("Fail connect : "+error);
        },  
        handleSuccess(org_response,file,files){
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


.input-size{
    width: 80%;
    border-radius: 4px;
    margin-right: 3vh!important;
    margin-left: 0px!important;
}

#form1{
    display: flex;
    flex-flow: column;
    width: 50%;
    margin: auto;
    padding: 0px;
}

.button{
    width: 5vh;
    margin-left: 0px!important;
    margin-right: 2vh!important;
}

#notice{
    font-size: 16px;
    user-select: none;
    margin-bottom: 2vh;
    margin-top: 5vh;
}

.center{
    margin: auto;
}

.fl{
    position: relative;
    top: 5vh;
    width: 60%;
    min-height: 5vh;
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

.bigger{
    scale: 1.2;
}
.item{
    width: 50%;
}
.upload{
    width: 5vh;
    padding: 0px;
}

.scale{
    scale: 1.3;
}

</style>