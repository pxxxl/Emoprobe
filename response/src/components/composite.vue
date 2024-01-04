<template>
    <div class="dis-flex direction-row-flex composite">
        <el-button @click="FileUpShow($event)" type="success" @mouseleave="(event) => event.target.blur()"
            class="uploadfilenbtn">
            <el-icon>
                <Upload />
            </el-icon>
        </el-button>
        <FileUp :visiable="vs" />
        <div class="backimg">
            <form id="form1" :style="{ boxShadow: `var(--el-box-shadow-dark)` }" class="center-flex">
                <!-- <span id="notice" class="dis-flex center-flex">{{ url_notice }}</span>  -->
                <div class="dis-flex direction-row-flex center-flex in">
                    <el-input v-model.lazy="video" type="textarea" :show-word-limit="true"
                        :autosize="{ minRows: 3, maxRows: 5 }" :autofocus="true" :clearable="true" class="input-size"
                        :placeholder="url_notice" :style="{ boxShadow: `var(--el-box-shadow-dark)` }" />

                    <el-button type="primary" native="button" class="button center"
                        @mouseleave="(event) => event.target.blur()" @click="Postdata">
                        <el-icon>
                            <Search class="scale" />
                        </el-icon>
                    </el-button>

                    <el-button type="primary" native="button" class="buttonD center"
                        @mouseleave="(event) => event.target.blur()" @click="getFile">
                        爬取评论 <el-icon>
                            <Download class="scale" style="margin-left: 3px;" />
                        </el-icon>
                    </el-button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { translateBV, ShowErrorMessage } from '@/assets/g.js'
import NothingShow from './NothingsShow.vue'
import FileUp from './fileUp.vue'

export default {
    data() {
        return {
            url_notice: "请输入分析对象视频的url或BV号",
            video: "",
            commitNotice: "提交",
            com: null,
            show: null,
            success: false,
            vs: false,
        }
    },
    components: {
        NothingShow,
        FileUp
    },
    methods: {
        getFile() {
            let bv_str = "";
            console.log("下载");
            bv_str = translateBV(this.video);
            if (bv_str == "error") {
                ShowErrorMessage("提取bv号出现错误");
                return;
            }
            axios.get("/api/v1/crawl", {
                params: {
                    bv: bv_str
                }
            }).then((org_response) => {
                let response = org_response.data;
                if (response.code == 407) {
                    ShowErrorMessage("爬取信息失败");
                    return;
                }
                const a = document.createElement('a');
                a.download = "数据结果" + bv_str + ".json";
                a.style.display = 'none';
                const blob = new Blob([JSON.stringify(response.data)]);
                a.href = URL.createObjectURL(blob);
                a.click();
                this.video = "";
            })
        },
        Postdata() {
            let bv_number = "";
            bv_number = translateBV(this.video);
            if (bv_number === "error") {
                ShowErrorMessage("提取bv号出现错误");
                return;
            }
            this.$router.push({
                path: "/datashow",
                query: { bv: bv_number }
            });
        },
        FileUpShow(event) {
            event.target.blur();
            this.vs = !this.vs;

        },
    },
    mounted() {
        this.uploadRef = this.$refs.uploadRef;
    },
}
</script>

<style scoped>
.backimg {
    width: 60%;
    margin: auto;
    padding: 1px;
    background-image: url('/resource/picture/blueArch.png');
    background-repeat: no-repeat;
    background-size: 100% 100%;
}

.in {
    width: 100%;
}

.composite {}

.uploadfilenbtn {
    position: absolute;
    top: 70px;
    right: 0px;
}

.input-size {
    width: 100%;
    border-radius: 4px;
    margin-right: 3vh !important;
    margin-left: 0px !important;
}

#form1 {
    display: flex;
    width: 85%;
    margin: auto;
    margin-top: 25vh;
    padding: 5px;
    height: 110px;
    backdrop-filter: blur(6px);
}

.button {
    width: 5vh;
    margin-left: 0px !important;
    margin-right: 2vh !important;
}

#notice {
    font-size: 16px;
    user-select: none;
    margin-bottom: 10px;
    margin-top: 10px;
}

.center {
    margin: auto;
}

.fl {
    position: relative;
    top: 5vh;
    width: 60%;
    min-height: 5vh;
}

.set-interval {
    margin-right: 1vh;
    flex: 1;
}

.name {
    font-size: large;
    flex: 7;
}

.icon {
    flex: 1;
}

.bigger {
    scale: 1.2;
}

.item {
    width: 50%;
}

.upload {
    width: 5vh;
    padding: 0px;
}

.scale {
    scale: 1.3;
}
</style>