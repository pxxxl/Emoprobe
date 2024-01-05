<template>
  <el-dialog v-model="dialogTableVisible" title="爬取评论文件">
    <el-input v-model="video" class="videoIn" @keyup.enter="getFile" placeholder="请输入分析对象视频的url或BV号"></el-input>
    <div class="dis-flex center-flex" style="margin-top: 10px;">
        <el-button @click="getFile" :loading="btn_load" :loading-icon="Eleme" type="primary">确定</el-button>
        <el-button @click="dialogTableVisible = false" :disabled="btn_load" type="primary">取消</el-button>
    </div>
  </el-dialog>
</template>

<script lang="ts" setup>
import axios from 'axios'
import { translateBV, ShowErrorMessage } from '@/assets/g.js'
import NothingShow from './NothingsShow.vue'
import { ref, watch } from 'vue';
import { vi } from 'element-plus/es/locale';
import { Eleme } from '@element-plus/icons-vue'

const dialogTableVisible = ref(false);
const video = ref("");
const btn_load = ref(false)

const props = defineProps(['visiable']);

const getFile= ()=> {
            let bv_str = "";
            console.log("下载");
            bv_str = translateBV(video.value);
            if (bv_str == "error") {
                ShowErrorMessage("提取bv号出现错误");
                return;
            }
            btn_load.value = true;
            axios.get("/api/v1/crawl", {
                params: {
                    bv: bv_str
                }
            }).then((org_response) => {
                let response = org_response.data;
                if (response.code == 407) {
                    btn_load.value = false;
                    ShowErrorMessage("爬取信息失败");
                    return;
                }
                const a = document.createElement('a');
                a.download = "数据结果" + bv_str + ".json";
                a.style.display = 'none';
                const blob = new Blob([JSON.stringify(response.data)]);
                a.href = URL.createObjectURL(blob);
                a.click();
                video.value = "";
                btn_load.value = false;
                dialogTableVisible.value = false;
            })
        }
watch(()=>props.visiable,async (newvalue,oldvalue)=>{
    dialogTableVisible.value = true;
})
</script>

<style>
.videoIn{
    width: 50%;
    margin-left: 50%;
    transform: translateX(-50%);
}
</style>