package com.minjer.service.impl;

import com.minjer.link.Crawler;
import com.minjer.link.EmotionModule;
import com.minjer.mapper.CommentMapper;
import com.minjer.mapper.VideoMapper;
import com.minjer.pojo.*;
import com.minjer.service.VideoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

@Service
public class VideoServiceImpl implements VideoService {
    @Autowired
    private VideoMapper videoMapper;
    private CommentMapper commentMapper;

    /**
     * 添加视频信息进入数据库
     * 待测试（接入爬虫和分析模型的测试）
     * 1.进行数据库查询，是否能找到对应视频，若找不到则继续，若找到则返回
     * 2.调用爬虫获取视频对象
     * 3.处理返回结果，调用情感处理模型
     * 4.将数据存入数据库中
     *
     * @param bv
     * @return 消息码
     * 200 成功
     * 405 数据库中已存在该视频
     * 406 出现错误
     */
    @Override
    public int addVideo(String bv) {
        int code = 406;
        // 检测数据库中是否存在该视频
        Video video = videoMapper.selectByBv(bv);
        if (video != null) {
            // 视频在数据库中已经存在
            code = 405;
        } else {
            // 调用爬虫爬取视频信息
            VideoComment videoComment = Crawler.getVideoWithComments(bv);

            // 爬取结果不为null说明爬取到了信息
            if (videoComment != null) {

                // 对爬虫结果解封装
                video = videoComment.getVideo();
                video.setVideoSavedate(LocalDateTime.parse(LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"))));
                List<Comment> comments = videoComment.getComments();

                // 提取文本内容出来
                List<String> rawData = new ArrayList<>();
                for (Comment comment : comments) {
                    rawData.add(comment.getCommentText());
                }

                // 向情感分析模块发送数据
                List<Sentence> handledData = EmotionModule.handleSentence(rawData);

                // 正确处理了所有消息并拿到结果
                if (handledData != null) {
                    // 将结果整合起来
                    for (int i = 0; i < comments.size(); i++) {
                        comments.get(i).setCommentEmotion(handledData.get(i).getSentenceEmotion());
                    }

                    // 向数据库中添加数据
                    videoMapper.addVideo(video);
                    commentMapper.addComments(comments);

                    code = 200;
                }
            }
        }
        return code;
    }

    /**
     * 根据视频bv号删除视频
     * 通过受影响行数判断是否删除成功
     *
     * @param bv
     * @return 消息码
     * 200 成功
     * 407 数据库中不存在该视频
     */
    @Override
    public int deleteVideo(String bv) {
        int ans = videoMapper.delByVideoBvid(bv);
        int code = 407;
        if (ans != 0) {
            return 407;
        }
        return code;
    }

    /**
     * 根据bv号更新视频信息
     * 待测试（接入爬虫和分析模型的测试）
     * 通过受影响行数判断是否更新成功
     * 1.进行删除操作，若返回为0则说明数据库中不存在该视频，直接返回
     * 2.调用addVideo方法，将视频信息重新分析并添加进数据库
     * @param bv
     * @return 消息码
     * 200 成功
     * 407 数据库中不存在该视频
     */
    @Override
    public int updateVideo(String bv) {
        int code = 407;
        if (videoMapper.delByVideoBvid(bv) != 0) {

            addVideo(bv);

            code = 200;
        }
        return code;
    }
}
