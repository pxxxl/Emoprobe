package com.minjer.link;

import com.alibaba.fastjson.JSON;
import com.minjer.pojo.Comment;
import com.minjer.pojo.VideoComment;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.time.LocalDateTime;

public class Crawler {
    /**
     * 调用爬虫爬取对应bv号视频
     * 此处不会对数据做额外处理，只做封装功能
     * 执行逻辑：
     * 1. 获取执行python爬虫的语句
     * 2. 调用Runtime.getRuntime().exec()方法执行python爬虫
     * 3. 等待子进程执行完成
     * 4. 读取子进程的输出流
     * 5. 将输出流转换为JSON对象
     * 6. 将JSON对象转换为VideoComment对象
     * 7. 返回VideoComment对象
     *
     * @param bv
     * @return 返回一个包含视频和评论信息的结果，如果爬取失败则返回null
     */
    public static VideoComment getVideoWithComments(String bv) {
        try {
            String currentWorkingDirectory = System.getProperty("user.dir");
            // 构建 crawler.py 文件的相对路径
            String pythonScript = "python ../crawler/crawler.py -bv " + bv;

            // 调用 python 爬虫
            Process process = Runtime.getRuntime().exec(pythonScript);
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            StringBuilder output = new StringBuilder();
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }

            // 打印输出流（测试用）
            System.out.println(output.toString());

            // 等待子进程执行完成
            int exitCode = process.waitFor();

            if (exitCode == 0 ) {
                // 爬虫执行成功
                VideoComment videoComment = JSON.parseObject(String.valueOf(JSON.parseObject(output.toString()).getJSONObject("data")), VideoComment.class);
                if (videoComment == null) {
                    return null;
                }
                videoComment.getVideo().setVideoSavedate(LocalDateTime.now());
                videoComment.getVideo().setVideoBvid(bv);
                for (int i = 0; i < videoComment.getComments().size(); i++) {
                    // 设置评论的视频bv号，与视频信息的bv号一致
                    videoComment.getComments().get(i).setVideoBvid(bv);
                }


                return videoComment;
            } else {
                return null;
            }
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

}
