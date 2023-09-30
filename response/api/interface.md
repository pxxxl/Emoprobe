#       InterFace DOC
 >this is a interface doc of front-to-back interaction

## InterFace 1
#### 通过用户输入的视频url获取该视频下评论并对该视频下的所有评论进行情感分析
<font color="aqua">请求方式</font>：POST

<font color="aqua">请求正文参数：</font>
|参数名|类型|注释|
|:---:|:---:|:---:|
|bv_url|str|请求爬取和分析的b站视频url地址或BV号|

<font color="aqua">返回参数（json格式）</font>

<b>root（根节点）</b>

|字段|类型|内容|注释|
|:---:|:---:|:---:|:---:|
|result|bool|分析成功与否|流程正常时为ture<br>出现错误时为false|
|analys|正确时：json <br> 错误时：null|分析结果|视频评论区的整体评论分析结果数据|
|error_mes|发生错误时（result值为false）：str <br>不发生错误时（result值为true）：null|错误信息|错误信息代码<br>000010<br>000011<br>000012<br>000002|

<b>analys</b>

|字段|类型|内容|注释|
|:---:|:---:|:---:|:---:|
|...|...|...|...|



## InterFace 2
#### 通过用户输入的评论在相应的视频下进行的情感分析
<font color="aqua">请求方式</font>：POST

<font color="aqua">请求正文参数：</font>
|参数名|类型|内容|注释|
|:---:|:---:|:---:|:---:|
|comment|str|单个评论句子|待分析的评论，由用户输入|
|bv|str|目标评论的视频|B站视频的BV号或url|

<font color="aqua">返回参数（json格式）</font>

<b>root（根节点）</b>

|字段|类型|内容|注释|
|:---:|:---:|:---:|:---:|
|result|bool|分析成功与否|流程正常时为true <br> 流程出错时为false|
|analys|正确时（result为true）：json <br> 错误时（result为false）：null|分析结果|......|
|error_mes|发生错误时（result值为false）：str <br>不发生错误时（result值为true）：null|错误信息|错误信息代码<br>100010<br>100011<br>100012<br>100002|

<b>analys</b>

|字段|类型|内容|注释|
|:---:|:---:|:---:|:---:|
|...|...|...|...|