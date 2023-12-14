package com.minjer.link;

import com.alibaba.fastjson.JSON;
import com.minjer.pojo.VideoComment;
import com.minjer.utils.Tool;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.time.LocalDateTime;

/**
 * 爬虫类
 *
 * @author Minjer
 */
@Slf4j
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
     * @param bv 视频bv号
     * @return 返回一个包含视频和评论信息的结果，如果爬取失败则返回null
     */
    public static VideoComment getVideoWithComments(String bv) {
        try {
            // 由于不同操作系统下路径很容易出现问题，所以这里使用绝对路径
            // 获取当前工作目录
            String currentWorkingDirectory = System.getProperty("user.dir");

            // 获取爬虫文件所在目录
            String headDirectory = Tool.traverseUp(currentWorkingDirectory, 1);

            // 获取执行python爬虫的语句
            String pythonScript = "python " + headDirectory + File.separator + "crawler" + File.separator + "crawler.py -bv " + bv + " -config " + headDirectory + File.separator + "crawler" + File.separator + "config.json";

            // 调用 python 爬虫
            Process process = Runtime.getRuntime().exec(pythonScript);

            // 读取子进程的输出流
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            StringBuilder output = new StringBuilder();
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }

//            log.info("Crawler output: " + output.toString());

            // 等待子进程执行完成
            int exitCode = process.waitFor();

            if (exitCode == 0) {
                // 爬虫执行成功
                VideoComment videoComment = JSON.parseObject(String.valueOf(JSON.parseObject(output.toString()).getJSONObject("data")), VideoComment.class);
                if (videoComment == null) {
                    log.info("Crawler return null");
                    // 爬虫执行成功，但是返回的数据为空
                    return null;
                }
//                log.info("Crawler return video: " + videoComment.getVideo().toString());
                // 设置视频的bv号，与传入的bv号一致，同时设置视频的保存时间
                videoComment.getVideo().setVideoSavedate(LocalDateTime.now());
                videoComment.getVideo().setVideoBvid(bv);

                // 设置评论的视频bv号，与视频信息的bv号一致
                for (int i = 0; i < videoComment.getComments().size(); i++) {
                    videoComment.getComments().get(i).setVideoBvid(bv);
                }

                log.info("Crawler return videoComment");
                return videoComment;
            } else {
                log.error("Crawler wrong");
                return null;
            }
        } catch (Exception e) {
            log.error("Crawler wrong");
            e.printStackTrace();
            return null;
        }
    }

}
