# 前端部署
### 环境配置和部署
**首先，你需要安装一个服务器环境。**

- [Nginx](https://nginx.org/en/)

- [Apache](https://apache.org/)

这两个服务器软件其中一个即可。

**然后，你需要获得打包好后的前端生产化实例**

1. 从github上clone或下载[response](../response)文件夹到本地
2. 使用终端进入到该文件夹的目录下

    > 也可以使用[vscode](https://code.visualstudio.com/)打开项目，在vscode的终端中进入该文件夹
3. 在终端中输入
```sh
#1、安装插件，只需执行一次
npm install
    #或者 
npm i

#2、构建生产化实例
npm run build
```
> 提示：指令的执行需要在本机提前安装好[Nodejs](https://nodejs.org)环境

4. 在response目录下即可获得dist文件，即为我们所需要的生产化实例

**最后，将实例部署在网站上**
- 只需要将上一步骤获取的到的dist文件里的所有的文件复制粘贴放置在网站的根目录上。

>Tips：假如你不想在服务器上运行该网站，只想在本地实现复现开发，那你只需要在将指令改为
```sh
#1、安装插件，只需执行一次
npm install
    #或者 
npm i

#2、构建开发实例
npm run dev
```

