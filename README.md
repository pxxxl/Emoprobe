# Emoprobe
随着移动互联网的普及，人们已经习惯于在网络上表达意见和建议，这些评价中都蕴含着巨大的商业价值。比如某品牌公司可以分析社交媒体上广大民众对该品牌的评价，如果负面评价忽然增多，就可以快速采取相应的行动。

Emoprobe，为解决该需求而诞生的项目。针对bilibili视频网站进行特化，可爬取bilibili绝大部分视频信息和相关评论内容，并且结合bilibili用户的语言习惯，给出评论的分析结果和可视化统计信息，帮助您更好了解人们的情绪倾向。



Emoprobe是一个免费开源项目，地址[Emoprobe，数据可视化的情感分析系统](https://github.com/pxxxl/Emoprobe)



Crawler support， thanks [@pxxxl](https://github.com/pxxxl)

DeepLearning support, thanks [@Sen-Yao](https://github.com/Sen-Yao)

BackEnd support, thanks [@mj3622](https://github.com/mj3622) 

FrontEnd support, thanks [@nianmobai](https://github.com/nianmobai)



![](https://img.shields.io/github/commit-activity/m/pxxxl/Emoprobe?color=4e4c97) ![](https://img.shields.io/tokei/lines/github/pxxxl/Emoprobe?color=4e4c97) ![](https://img.shields.io/github/repo-size/pxxxl/Emoprobe?color=4e4c97)  

这是一张Web预览图

![前端页面](docs/pics/main_page.png)

## 功能 Features

- **爬取信息：** bilibili视频信息，用户评论
- **情感分析：** 支持用户上传视频信息，直接输入视频连接，直接输入待分析文字等方式进行分析
- **数据统计：** 针对分析结果可进行数据筛选，查看可视化统计图表

**突出特性：**

- **正则匹配：** 可直接通过输入视频连接提取BV号

- **语境特化：** 针对biilibili网站用户群体的语言习惯对模型进行了优化

- **文件操作：** 可下载和上传爬虫爬取的视频文件

- **远程部署：** 本项目已支持并成功部署在服务器上，欢迎大家体验 [Emoprobe System](http://116.204.9.108/#/)

  

## 部署 Deploy

本项目采用前后端分离的B/S架构，我们可以通过如下方式进行项目的部署

- **Docker部署：** 开发中
- **手动部署：** 可参考以下文档进行项目部署
  - 后端部署：[后端部署教程](docs/backend_deploy.md)
  - 前端部署：[前端部署教程](docs/frontend_deploy.md)
  - Python环境：[Python环境搭建教程](docs/python_deploy.md)

## 如何上报bug How to Report Bugs

在提问题之前，请至少花费5分钟来思考和准备，确认是由系统错误引起的bug

- 若是部署过程中出现问题，请先再次阅读部署教程
- 上传错误log，位于`BackEnd/log`文件夹下，请找到ERROR部分的日志，并和出错页面详细情况截图一并上传



## 参与开发 Join Development

Emoprobe仍在不断优化中，如果您有参与开发的意愿，欢迎向 Emopeobe提交 [Pull Requests](https://github.com/pxxxl/Emoprobe/pulls)，我们会认真阅读你的每一行代码的。
