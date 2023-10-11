<template>
    <div id="select-part" class="">
        <select v-model="enter" id="select" @change="$emit('select',select)">
            <option value="selectA">{{fun1}}</option>
            <option value="selectB">{{fun2}}</option>
        </select>
        <!-- <button type="button" id="selectA" @click="Func1">{{ fun1 }}</button> -->
        <!-- <button type="button" id="selectB" @click="Func2"> {{ fun2 }} </button> -->
    </div>
</template>

<script>
export default{
    data() {
        return {
            fun1:"单个评论分析",
            fun2:"视频评论分析",
            enter:"selectA",
            select:true
        }
    },
    methods:{
    },
    watch:{
        enter(newValue){
           if(newValue == "selectA")this.select = true;
           if(newValue == "selectB") this.select = false;
        }
    }
}
</script>

<style scoped>

#select{
    height: 30px;
    width: 200px;
}

#select-part{
    position: absolute;
    height: 80px;
    width: 200px;
    top: 0;
    right: 5%;
    transform: translateX(-50%);
    background-color: var(--color-button);
}
</style>