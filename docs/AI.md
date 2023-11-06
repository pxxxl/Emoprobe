# AI情绪感知接口

## 命令行调用

**使用方法**
> python emotion_detect.py 

**命令行参数选项**

* -i <以json字符串组织的评论列表>：（必填，与-fi互斥）添加后将读取此json字符串，作为评论列表（json字符串格式见下）
* -fi <json文件路径>：（必填，与-i互斥）：添加后将读取文件指定路径的json文件，作为评论列表读取（json字符串格式见下）
* -o <文件保存路径>：（非必填项）添加后，视频信息将不再打印到标准输出，而是保存到指定路径的文件，如果路径上已经存在文件，则原本文件的内容将被覆盖。

其中，无论命令行选项是-i还是-fi，读取的json字符串均以这种形式组织：

根对象：
| 字段    | 类型 | 内容     | 备注                          |
| ------- | ---- | -------- | ----------------------------- |
| comments | list  | 评论字符串列表 |                       |

其中，comments是字符串类型的列表，每一个字符串代表一条评论。

**效果**

将从标准输出打印结果字符串，字符串以json格式组织，内容如下。

根对象：
| 字段    | 类型 | 内容     | 备注                          |
| ------- | ---- | -------- | ----------------------------- |
| emotions    | list  | 情绪字符串列表   |   |

其中，emotions是字符串的列表，每一个字符串代表一条情绪分析结果，emotions列表与输入的comments列表是等长的，而且给定下标i，emotions[i]对应comments[i]的分析结果。

如果调用时指定-o参数，则不会打印到标准输出，而是输出到文件。