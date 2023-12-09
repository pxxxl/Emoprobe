<template>
    <div class="sift-button dis-flex align-items-center">
        <div class="dis-flex direction-column-flex center-flex">
            <el-button @click="AddSift" style="margin-bottom:1vh ;" @mouseleave="(event)=>{event.target.blur()}">
                筛选
            </el-button>
            <el-button @click="ClearAll" style="margin-top: 1vh;" @mouseleave="(event)=>{event.target.blur()}">
                清空筛选
            </el-button>
        </div>
                <div class="ip-select">
                   <h3 class="left-float">ip</h3>
                   <div class="ipshow">
                    <el-tag
                        v-for="tag in dynamicTags"
                        :key="tag"
                        class="tag"
                        closable
                        :disable-transitions="false"
                        @close="handleClose(tag)"
                    >
                        {{ tag }}
                    </el-tag>
                    <el-input
                        v-if="inputVisible"
                        ref="InputRef"
                        v-model="inputValue"
                        class="ip-input"
                        size="small"
                        @keyup.enter="handleInputConfirm"
                        @blur="handleInputConfirm"
                    />
                    <el-button v-else class="button-new-tag" size="small" @click="showInput">
                        +输入ip
                    </el-button>
                    </div>
                </div>
                <div class="gender-select">
                    <h3>性别筛选</h3>
                    <el-checkbox-group v-model="gender">
                        <el-checkbox label="男" />
                        <el-checkbox label="女" />
                        <el-checkbox label="保密" />
                    </el-checkbox-group>
                </div>
                <div class="date-select">
                    <h3>日期</h3>
                    <el-date-picker
                        v-model="date"
                        type="datetimerange"
                        start-placeholder="开始时间"
                        end-placeholder="结束时间"
                        format="YYYY-MM-DD HH:mm:ss"
                        date-format="YYYY/MM/DD ddd"
                        time-format="hh:mm:ss"
                        value-format="YYYY-MM-DD HH:mm:ss"
                        style="width: 90%!important;"
                        @change="DateToString(date)"
                    />
                </div>
                <div class="like-select">
                    <h3>点赞数</h3>
                    <div class="dis-flex direction-row-flex align-items-center">
                        <el-input-number v-model.lazy="like[0]" class="num-input" :controls="false" :precision="0" :max="like[1]"/><el-icon size="3vh"><Minus /></el-icon>
                        <el-input-number v-model.lazy="like[1]" class="num-input" :controls="false" :precision="0" :min="like[0]"/>
                    </div>
                </div>
                <div class="reply-select">
                    <h3>回复数</h3>
                    <div class="dis-flex direction-row-flex align-items-center">
                        <el-input-number v-model.lazy="reply[0]" class="num-input" :controls="false" :precision="0" :max="reply[1]"/><el-icon size="3vh"><Minus /></el-icon>
                        <el-input-number v-model.lazy="reply[1]" class="num-input" :controls="false" :precision="0" :min="reply[0]"/>
                    </div>
                </div>
                <div class="emotion-select">
                    <h3>情感</h3>
                    <el-checkbox-group v-model="emotion">
                    <el-checkbox label="快乐"/>
                    <el-checkbox label="愤怒"/>
                    <el-checkbox label="厌恶"/>
                    <el-checkbox label="恐惧"/>
                    <el-checkbox label="悲伤"/>
                    </el-checkbox-group>
                </div>
    </div>
</template>

<script lang="ts" setup>
import { nextTick, onMounted, ref, watch} from 'vue';
import { ElInput } from 'element-plus'
import { da, es, tr } from 'element-plus/es/locale';
const emit = defineEmits(['sift'])

const inputVisible = ref(false);
const inputValue = ref("");
const InputRef = ref<InstanceType<typeof ElInput>>();

const dynamicTags = ref(Array());
const date = ref(null);//date
const gender = ref(new Array("男","女","保密"));
const like = ref(Array<number|null>(2));
const reply = ref(Array<number|null>(2));
const emotion = ref(Array<string>());

const date_string = ref("");
const emotion_string = ref("");
const like_string = ref("");
const reply_string = ref("");

const handleInputConfirm=()=>{
    if(inputValue.value){
        dynamicTags.value.push(inputValue.value);
    }
    inputVisible.value = false;
    inputValue.value = '';
}

const showInput = ()=>{
    inputVisible.value = true;
    nextTick(()=>{
        InputRef.value?.input?.focus();
    });
}

const handleClose = (tag:string)=>{
    dynamicTags.value.splice(dynamicTags.value.indexOf(tag), 1);
}


const DateToString=(value:string[]|null)=>{
    if(value)date_string.value = value[0] + ',' + value[1];
    else date_string.value = "";
}

const LikeToString = (value:(number|any)[])=>{
    let v1:string = (value[0]==null)?"":value[0].toString();
    if(value[1]) like_string.value = v1 + "," + value[1].toString();
    else like_string.value = v1;
}

const ReplyToString = (value:(number|null)[])=>{
    let v1:string = (value[0]==null)?"":value[0].toString();
    if(value[1]) reply_string.value = v1 + "," + value[1].toString();
    else reply_string.value = v1;
}

const ClearAll = ()=>{
    dynamicTags.value = [];
    gender.value = ["男","女","保密"];
    date.value = null;
    like.value = [null,null];
    reply.value = [null,null];
    emotion.value = [];
    AddSift();
}
const AddSift = ()=>{
    DateToString(date.value);
    LikeToString(like.value);
    ReplyToString(reply.value);
    emit('sift',dynamicTags.value.toString()
        ,gender.value.toString()
        ,date_string.value
        ,like_string.value
        ,reply_string.value
        ,emotion.value.toString()
    );
}
</script>

<style scoped>
.ip-select{
    flex: 1;
    margin-right: 1vh;
    margin-left: 1vh;
}

.gender-select{
    flex: 1;
}

.date-select{
    flex: 1;
}

.like-select{
    flex: 1;
}

.reply-select{
    flex: 1;
}

.emotion-select{
    flex: 1;
}

.tag{
    min-width: 3vh;
    margin: 0.5vh;
}

.button-new-tag{
    min-width: 3vh;
    margin-left: 1.5vh;
}

.ip-input{
    width: 10vh;
    margin-left: 1.5vh;
}

.ipshow{
    margin-left: 0.5vh;
}

.num-input{
    width: 8vh;
}
</style>