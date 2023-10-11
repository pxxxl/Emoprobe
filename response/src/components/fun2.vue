<template>
    <form v-if="op2">
        <span>{{ video_target_notice}} </span> <input type="text" v-model.lazy="commet">
        <p>{{ commet }}</p>
        <span> {{ comment_notice }} </span> <input type="text" v-model.lazy="video">
        <p>{{ video }}</p>
        <button>{{ commitNotice }}</button>

        <func2Chart />
    </form>

</template>

<script>
import func2Chart from './func2Chart.vue';
import axios from 'axios';

export default{
    data() {
        return {
            video_target_notice:"目的视频的url或BV号",
            comment_notice:"待分析的评论",
            commet:"",
            video:"",
            commitNotice:"提交"
        }
    },
    props:["op2"],
    components:{
        func2Chart
    },
    methods:{
        Postdata(){
            let postdata;
            postdata.video = this.video;
            postdata.comment = this.commet;
            if(postdata.video[0] != 'B' || postdata.video[1] != 'V')
                postdata.video = translateBV(postdata.video);
            let Interface =  getInterFace();
            axios.post(Interface,JSON.stringify(postdata))
            .then(function (response) {  
                //TODO
                //show data's chart
            }).catch((error)=>{
                console.log("error:posting data" + error);
            });
        }
    }
}

function getInterFace(){
    let Inter = null;
        axios.get('@public/api.json')
        .then(function (response) { 
            console.log(response);
            let re = JSON.parse(response);
            Inter = re.interface2_url;
        }).catch((error)=>{ console.log("error:getting interface" + error)});
    return Inter;
}
</script>