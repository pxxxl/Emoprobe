<template>
    <div class="">
        <div class="dis-flex direction-row-flex align-items-center">
            <span style="margin-left: 10px; margin-right: 2px;">ip</span>
            <el-select v-model="ip" placeholder="ip选择" :multiple="true">
                <el-option value="">无</el-option>
                <el-option v-for="item in ipArr" :value="item">{{item}}</el-option>
            </el-select>
            <span style="margin-left: 100px; margin-right: 2px;">日期</span>
            <el-date-picker
                v-model="org_date"
                type="datetimerange"
                start-placeholder="开始时间"
                end-placeholder="结束时间"
                value-format="YYYY-MM-DD HH:mm:ss"
                date-format="YYYY/MM/DD ddd"
                time-format="hh:mm:ss"
                label-format="YYYY-MM-DD HH:mm:ss"
                style="
                    margin-right: 400px!important;
                    margin-left: 2px;
                "
                @change="DateToString"
            />
            <el-button class="moresift"  @click="siftShow = !siftShow" @mouseleave="(event)=>event.target.blur()">
            更多筛选
                <el-icon v-if="!siftShow"><ArrowDown /></el-icon>
                <el-icon v-if="siftShow"><ArrowUp /></el-icon>
            </el-button>
        </div>
        <transition name="morepart">
            <div v-if="siftShow" class="ms">
                <div id="gender-sift" class="dis-flex align-items-center direction-row-flex">
                    <span class="notice-sp">性别</span>
                    <el-radio-group v-model="gender" size="large">
                        <el-radio-button label="" class="margin-tblr">无筛选</el-radio-button>
                        <el-radio-button label="男"  class="margin-tblr"></el-radio-button>
                        <el-radio-button label="女"  class="margin-tblr"></el-radio-button>
                        <el-radio-button label="未知"  class="margin-tblr"></el-radio-button>
                    </el-radio-group>
                </div>
                <div id="like-sift" class="dis-flex align-items-center direction-row-flex">
                    <span class="notice-sp">点赞数</span>
                    <el-radio-group v-model="like" size="large">
                        <el-radio-button  label=""  class="margin-tblr">无筛选</el-radio-button>
                        <el-radio-button label="0,50"  class="margin-tblr">0-50</el-radio-button>
                        <el-radio-button label="51,200"  class="margin-tblr">50-200</el-radio-button>
                        <el-radio-button label="201,1000"  class="margin-tblr">200-1000</el-radio-button>
                        <el-radio-button label="1001,"  class="margin-tblr">1000以上</el-radio-button>
                    </el-radio-group>
                </div>
                <div id="reply-sift" class="dis-flex align-items-center direction-row-flex">
                    <span class="notice-sp">回复数</span>
                    <el-radio-group v-model="reply" size="large">
                        <el-radio-button  label=""  class="margin-tblr">无筛选</el-radio-button>
                        <el-radio-button label="0,50"  class="margin-tblr">0-50</el-radio-button>
                        <el-radio-button label="51,200"  class="margin-tblr">50-200</el-radio-button>
                        <el-radio-button label="201,1000"  class="margin-tblr">200-1000</el-radio-button>
                        <el-radio-button label="1001,"  class="margin-tblr">1000以上</el-radio-button>
                    </el-radio-group>
                </div>
                <div id="emotion-sift" class="dis-flex align-items-center direction-row-flex">
                    <span class="notice-sp">情感</span>
                    <el-checkbox-group v-model="emotion" size="small" >
                        <el-checkbox  label="快乐"  class="margin-tblr"/>
                        <el-checkbox  label="愤怒"  class="margin-tblr"/>
                        <el-checkbox label="厌恶"  class="margin-tblr"/>
                        <el-checkbox  label="恐惧"  class="margin-tblr"/>
                        <el-checkbox  label="悲伤"  class="margin-tblr"/>
                    </el-checkbox-group>
                </div>
            </div>
        </transition>
        
    </div>
</template>

<script lang="ts" setup>
import { nextTick, onMounted, ref, watch} from 'vue';
import { ElInput } from 'element-plus'
import { da, es, tr } from 'element-plus/es/locale';
const emit = defineEmits(['sift']);
const props =   defineProps(['ipArr']);
const ipArr = ref();

const ip = ref([])
const emotion = ref([]);
const like = ref('');
const reply = ref('');
const date = ref('');
const gender = ref("");

const org_date = ref(null);
const siftShow = ref(false);


const DateToString=(value:string[]|null)=>{
    if(value)date.value = value[0] + ',' + value[1];
    else date.value = "";
    console.log(date.value);
}

const ClearAll = ()=>{
    AddSift();
}
const AddSift = ()=>{
    emit('sift',ip.value.toString(),gender.value,date.value,like.value,reply.value,emotion.value.toString());
}
const CheckDate = (dd):boolean=>{
    // console.log(dd);
    return true;
}

watch([ip,gender,date,like,reply,gender,emotion],()=>{
    AddSift();
},{
    flush: 'post'
})

onMounted(()=>{
    ipArr.value = props.ipArr;
})
</script>

<style scoped>
.morepart-enter-active {
  animation: bounce-in 0.28s;
}
.morepart-leave-active {
  animation: bounce-in 0.28s reverse;
}

@keyframes bounce-in{
    0%{
        transform: scaleY(0)
    }
    10%{
        transform: scaleY(0.1)
    }
    20%{
        transform: scaleY(0.2)
    }
    25%{
        transform: scaleY(0.25)
    }
    40%{
        transform: scaleY(0.4)
    }
    50%{
        transform: scaleY(0.5)
    }
    60%{
        transform: scaleY(0.6)
    }
    75%{
        transform: scaleY(0.75)
    }
    80%{
        transform: scaleY(0.8)
    }
    100%{
        transform: scaleY(1)
    }
}

.ms{
    overflow: hidden;
    transform-origin: top;
}
.moresift{
    float: right;
}
#gender-sift{
    height: 6vh;
    width: 100%;
    margin-top: 2vh;
    margin-bottom: 1vh;
}
#like-sift{
    height: 6vh;
    width: 100%;
    margin-top: 2vh;
    margin-bottom: 1vh;
}
#reply-sift{
    height: 6vh;
    width: 100%;
    margin-top: 2vh;
    margin-bottom: 1vh;
}
#emotion-sift{
    height: 6vh;
    width: 100%;
    margin-top: 2vh;
    margin-bottom: 1vh;
}
.margin-tblr{
    margin-top: 3px;
    margin-bottom: 3px;
    margin-left: 4px;
    margin-right: 4px;
}
.notice-sp{
    font-size:15px;
    margin-right:3px;
}
</style>