//global function
function translateBV(url){
    const pre = "BV.*?/";
    let BV_num = url.match(pre);
    BV_num = BV_num[0].slice(0,12);
    return BV_num;
}