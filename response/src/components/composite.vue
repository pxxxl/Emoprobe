<template>
    <div class="dis-flex direction-column-flex composite">
        <FileUp :visiable="vsu" />
        <FileDown :visiable="vsd"/>
        <div class="backimg"></div>
            <form id="form1" class="center-flex direction-column-flex">
                <!-- <span id="notice" class="dis-flex center-flex">{{ url_notice }}</span>  -->
                <div class="dis-flex direction-row-flex center-flex in">
                    <el-input v-model.lazy="video" :show-word-limit="true"
                        :autofocus="true" :clearable="true" class="input-size"
                        :placeholder="url_notice" 
                        size="large"
                    />
                    <el-button type="primary" native="button" class="button center"
                        @mouseleave="(event) => event.target.blur()" @click="Postdata">
                        <el-icon>
                            <Search class="scale" />
                        </el-icon>
                    </el-button>
                </div>
                <div style="margin-top: 20px;">
                    <el-button  native="button" id="buttonD" class="center"
                        @mouseleave="(event) => event.target.blur()" @click="FileDownShow($event)">
                        爬取评论文件
                        <el-icon>
                            <Download class="scale" style="margin-left: 3px;" />
                        </el-icon>
                    </el-button>

                    <el-button @click="FileUpShow($event)"  @mouseleave="(event) => event.target.blur()"
                        id="buttonU" >
                        上传评论文件
                        <el-icon>
                            <Upload />
                        </el-icon>
                    </el-button>
                </div>
            </form>
    </div>
</template>

<script>
import { translateBV, ShowErrorMessage } from '@/assets/g.js'
import NothingShow from './NothingsShow.vue'
import FileUp from './fileUp.vue'
import FileDown from './fileDown.vue'

export default {
    data() {
        return {
            url_notice: "请输入分析对象视频的url或BV号",
            video: "",
            commitNotice: "提交",
            com: null,
            show: null,
            success: false,
            vsu: false,
            vsd:false
        }
    },
    components: {
        NothingShow,
        FileUp,
        FileDown
    },
    methods: {
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
            document.getElementById('buttonU').blur();
            this.vsu = !this.vsu;

        },
        FileDownShow(event) {
            event.target.blur();
            document.getElementById('buttonD').blur();
            this.vsd = !this.vsd;
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
    height: 200px;
    background-image: url('/resource/picture/blueArch.png');
    background-repeat: no-repeat;
    background-size: 100% 100%;
    margin-top: 1vh;
}

.in {
    width: 100%;
}

.composite {}

.input-size {
    width: 100%;
    border-radius: 4px;
    margin-right: 3vh !important;
    margin-left: 0px !important;
}

#form1 {
    display: flex;
    width: 60%;
    margin: auto;
    padding: 5px;
    height: 110px;
    backdrop-filter: blur(6px);
    border-radius: 10px;
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