<template>

    <FUNC_SELECT @select ="SelectChange" :bs="true"/>
    <div class="container">
        <div class="dis-flex direction-row-flex global">
            <div id="navigate">
                <VideoList />
            </div>
            <div id="mainpart">
                <composite v-if="select == 1"/>
                <single v-if="select == 2"/>
                <BACKTOP />
            </div>
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
    }
    </style>