<template>
    <div v-if="op1">
    <form>
       <span>{{ url_notice }}</span> <input type="text" v-model.lazy="video">
       <p>{{ video }}</p>
       <button>{{ commitNotice }}</button>
    </form>
    <func1Chart v-bind:comment_arr = "com" v-bind:chart_data = "show"/>
    </div>
</template>

<script>
import func1Chart from './func1Chart.vue'//import the component
import axios from 'axios'

export default{
    data() {
        return {
            url_notice:"请输入分析对象视频的url",
            video:"",
            commitNotice:"提交",
            com:null,
            show:null
        }
    },
    components:{
        func1Chart
    },
    props:["op1"],
    methods: {
        Postdata(){
            let Interface = this.getInterFace();
            let postdata = this.video;
            if(postdata.video[0] != 'B' || postdata.video[1] != 'V')
                postdata.video = translateBV(postdata.video);
            axios.post(Interface,JSON.stringify(postdata))
            .then(function (response){
                let result = JSON.parse(response);
                if(result == null){
                    console.log(console.error());
                    alert("接收数据错误");
                }
                this.com = result.data;
                //TODO
            }).catch((error) => {
                console.log("error:posting data" + error);
            });
        },
         getInterFace(){
            let Inter = null;
            axios.get('@public/api.json')
            .then(function (response) { 
            console.log(response);
            let re = JSON.parse(response);
            Inter = re.interface1_url;
            }).catch((error)=>{ console.log("error:getting interface" + error)});
            return Inter;
        }
    }
}
</script>