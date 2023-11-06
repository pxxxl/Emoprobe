<template>

<FUNC_SELECT @select ="SelectChange" />
<div id="mainpart">
<FUN1  v-if="select == 0"/>
<FUN2  v-if="select == 1"/>
<FUN3 v-if="select == 2"/>

<BACKTOP />
</div>

</template>

<script>
import FUNC_SELECT from '@/components/fun_select.vue'
import FUN1 from '@/components/fun1.vue'
import FUN2 from '@/components/fun2.vue'
import BACKTOP from '@/components/backtop.vue'
import FUN3 from '@/components/fun3.vue'

export default{
    data(){
        return {
            select:null
        }
    },
    components:{
        FUNC_SELECT,
        FUN1,
        FUN2,
        BACKTOP,
        FUN3
    },
    methods: {
        SelectChange(re){
            // console.log("触发成功，" + re);
            this.select = re;
        }
    },
}
</script>

<style scoped>
#mainpart{
    margin-left: 10%;
    margin-right: 10%;
    min-height: 90vh;
    background-color: var(--color-Appmainpart);
}
</style>