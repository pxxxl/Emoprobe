<template>

    <FUNC_SELECT @select ="SelectChange" />
    <div class="dis-flex direction-row-flex global">
        <div id="navigate" class="dis-flex justify-content-center border">
            <VideoList />
        </div>
        <div id="mainpart">
            <composite v-if="select == 1"/>
            <single v-if="select == 2"/>
            <BACKTOP />
        </div>
    </div>
    
    </template>
    
    <script>
    import FUNC_SELECT from './fun_select.vue'
    import composite from './composite.vue' 
    import BACKTOP from './backtop.vue'
    import single from './single.vue'
    import VideoList from './VideoList.vue'
    
    export default{
        data(){
            return {
                select:1
            }
        },
        components:{
            FUNC_SELECT,
            composite,
            BACKTOP,
            single,
            VideoList
        },
        methods: {
            SelectChange(re){
                this.select = re;
            }
        },
    }
    </script>
    
    <style scoped>
    #mainpart{
        flex: 8;
        background-color: var(--color-Appmainpart);
    }

    #navigate{
        flex: 2;
        border-radius: 3vh;
    }
    .global{
        min-height: 90vh;
        margin: 0px;
        padding: 0px;
    }
    </style>