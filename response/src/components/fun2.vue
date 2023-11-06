<template>
    <div class="border post">
        <form>  
            <el-upload 
                class="border size-pos-upload center-flex direction-column-flex"
                ref="uploadRef"
                :action="api"
                :limit="1" accept=".json" 
                :before-upload="beforeUpload" 
                :auto-upload="false" 
                :show-file-list="false"
                v-model:file-list="filelist"
                :on-exceed="handleExceed"
                :on-change="handelChange"
                :on-error="handleError"
                >
                <template #trigger>
                    <el-button slot="trigger" class="select-file-elbutton border" type="default" @mouseleave="(event)=>event.target.blur()">选择文件</el-button>
                </template>
                <div v-if="filelist.length > 0" class="fl">
                    <upload-item v-for="file in filelist" 
                                :file="file" 
                                :key="file.uid" 
                                :status="file.status"
                                >
                                    <template #file>
                                        <el-icon class="set-interval"><Document /></el-icon>
                                        <div>{{ file.name }}</div>
                                    </template>
                                    <template #elprogress>
                                        <el-icon @click="handleDelete"><Delete /></el-icon>
                                    </template>
                                     <el-progress :percentage="file.percentage" :status="file.status" :duration="5"/> 
                    </upload-item>
                </div>
                <el-button type="primary" class="post-file-elbutton" @click="submitUpload" @mouseleave="(event)=>event.target.blur()">提交</el-button>
            </el-upload>
        </form>
    </div>
    <func2Chart />
    <NothingShow />
</template>

<script>
import func2Chart from './func2Chart.vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import {getInterFace,ShowErrorMessage} from '@/assets/g.js';
import uploadItem from './upload-item.vue';
import NothingShow from './NothingsShow.vue'

// import { Comment, ref } from 'vue'
export default{
    data() {
        return {
            commitNotice:"提交",
            api:"",
            filelist:[],
            uploadRef:null,
        }
    },
    props:["op2"],
    components:{
        func2Chart,
        ElMessage,
        uploadItem,
        NothingShow
    },
    methods:{
        beforeUpload(file){
            let isJSON = file.type == 'application/json';
            console.log(file.type);
            if(!isJSON){
                ShowErrorMessage("请上传json格式的文件");
                return false;
            }
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
        submitUpload() {
            this.uploadRef.submit();
        },
        handleError(error, uploadFile, uploadFiles){
            ShowErrorMessage("Fail connect : "+error);
        },
        handleSuccess(response,file,files){
            console.log(response);
            //TODO
        },
        handleDelete(){
            this.filelist = [];
        }
    },
    mounted() {
       this.uploadRef = this.$refs.uploadRef;
       getInterFace(2).then((result) => {
        this.api = result;
       }).catch((err) => {
           ShowErrorMessage(err);
       });
    },
}
</script>

<style scoped>
.post{
    margin: auto;
    min-height: 20vh;
    width: 40%;
}
.size-pos-upload{
    min-height: 30%;
    width: 100%;
    display: flex;
}
.select-file-elbutton{
   margin-top: 10px!important;
   margin-bottom: 20px!important;
}
.post-file-elbutton{
    margin-top: 10px!important;
    margin-bottom: 10px!important;
}
.fl{
    width: 60%;
    min-height: 2vh;
}
.set-interval{
    margin-right: 1vh;
}
</style>