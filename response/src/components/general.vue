<template>
    <div style="min-height: 100vh;" class="dis-flex direction-column-flex">
        <div class="head">
            <FUNC_SELECT @select ="SelectChange" :bs="true"/>
        </div>
    <div class="container">
        <div class="dis-flex direction-row-flex global">
            <div id="navigate">
                <VideoList />
            </div>
            <div id="mainpart">
                <composite v-if="select == 1"/>
                <single v-if="select == 2"/>
                <fileup v-if="select == 3"></fileup>
            </div>
        </div>
    </div>
    </div>
    </template>
    
    <script>
    import FUNC_SELECT from './fun_select.vue'
    import composite from './composite.vue' 
    import single from './single.vue'
    import fileup from './fileUp.vue'
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
            single,
            VideoList,
            fileup
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
    }

    #navigate{
        flex: 2;
    }
    .global{
        min-height: 88vh;
        margin-left: 30px;
        margin-right: 30px;
        padding: 0px;
    }
    .container{
        background-image: url('/resource/picture/back.jpg');
        background-repeat: no-repeat;
        background-size:cover;
        flex: 1;
    }
    .head{
        flex-shrink: 0;
    }
    </style>