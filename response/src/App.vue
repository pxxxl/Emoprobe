<template>

<FUNC_SELECT @select ="(re)=>select = re" />
<FUN1 v-bind:op1 ="select" />
<FUN2 v-bind:op2="!select"/>

</template>

<script>
import FUNC_SELECT from '@/components/fun_select.vue'
import FUN1 from '@/components/fun1.vue'
import FUN2 from '@/components/fun2.vue'
export default{
    data(){
        return {
            select:true
        }
    },
    components:{
        FUNC_SELECT,
        FUN1,
        FUN2
    }
}
</script>