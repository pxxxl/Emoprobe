# 后端部署

在运行后端程序之前，我们需要做如下准备

## 1. 配置Java环境

对于Java环境的配置，此处提供两种解决方案

**方案一（推荐）：**

1. 安装JDK11以上的版本
2. 修改`‪BackEnd\BackEnd.jar\BOOT-INF\classes\application.yml`文件中的配置信息，**确保MySQL数据库的配置与本机保持一致**

**方案二：**

1. 安装IntelliJ IDEA 2021以上的版本
2. 通过IDEA以BackEnd文件夹作为项目根目录打开（若以其他文件夹为根目录，则会导致相对路径出错）
3. 接着利用IDEA内部集成的JDK和Maven，按照提示进行下载
4. 在下载完成后，进入`BackEnd/src/main/resources/application.yml`文件，可针对IP地址和端口进行修改，**并且修改MySQL数据库配置为本机配置**

## 2. 配置MySQL

确保本机已安装MySQL8.0以上的版本并且进程正在运行

1. 以root用户登录MySQL终端

2. 在终端中运行执行`BackEnd/emoprobe.sql`文件，具体命令为`SOURCE <sql文件路径>`

3. 在上述完成后，可通过如下语句确认是否配置完成：

   ```sql
   // 分别执行以下两条语句
   use emoprobe;
   show tables;
   
   // 若出现如下结果，说明成功配置
   +--------------------+
   | Tables_in_emoprobe |
   +--------------------+
   | comment            |
   | sentence           |
   | video              |
   +--------------------+
   3 rows in set (0.00 sec)
   ```

   

## 3. 运行后端项目

在经历完上述的配置之后，我们即可运行后端项目了



由于上文中给出了两种Java环境的配置方案，因此下面分别介绍两种方案的启动方式：

**方案一：** 使用使用命令行工具，在Backend文件夹下运行`java -jar .\BackEnd.jar`

**方案二：** 在IDEA中运行`BackEnd/src/main/java/com/minjer/BackEndApplication.java`文件



若控制台输出SpringBoot图像，则说明程序启动成功
