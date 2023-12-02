package com.minjer.service.impl;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.minjer.link.Crawler;
import com.minjer.link.EmotionModule;
import com.minjer.mapper.CommentMapper;
import com.minjer.mapper.VideoMapper;
import com.minjer.pojo.*;
import com.minjer.service.VideoService;
import com.minjer.utils.Tool;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class VideoServiceImpl implements VideoService {
    @Autowired
    private VideoMapper videoMapper;
    @Autowired
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
                video.setVideoSavedate(LocalDateTime.now());
                List<Comment> comments = videoComment.getComments();

                // 提取文本内容出来
                List<String> rawData = new ArrayList<>();
                for (Comment comment : comments) {
                    rawData.add(comment.getCommentText());
                }

                // 向情感分析模块发送数据
                List<String> handledData = EmotionModule.handleSentence(rawData);

                // 正确处理了所有消息并拿到结果
                if (handledData != null && handledData.size() != 0) {
                    // 将结果整合起来
                    for (int i = 0; i < comments.size(); i++) {
                        comments.get(i).setCommentEmotion(handledData.get(i));
                    }

                    // 向数据库中添加数据
                    videoMapper.addVideo(video);
                    batchInsertComments(comments);

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
     *
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

    /**
     * 根据bv号获取视频信息
     * 待测试（add方法）
     * 1.先查找数据库中是否存在该视频
     * 2.若存在则返回，若不存在则根据autopost判断是否进行爬取
     * 3.若autopost为1则调用addVideo方法进行爬取
     *
     * @param bv       bv号
     * @param autopost 是否会爬取信息
     *                 1 会
     *                 0 不会
     * @return 视频信息（若无未找到data域则为null）
     */
    @Override
    public Result getVideoInfo(String bv, int autopost) {
        int code = 408;
        VideoComment videoComment = new VideoComment();

        // 先查找数据库中是否存在该视频
        Video video = videoMapper.selectByBv(bv);

        // 若存在则返回，若不存在则根据autopost判断是否进行爬取
        if (video == null && autopost == 0) {
            code = 407;
            videoComment = null;
        } else {
            if (video == null) {
                addVideo(bv);
                video = videoMapper.selectByBv(bv);
            }

            List<Comment> comments = commentMapper.selectAllByVideoBvid(bv);

            videoComment.setVideo(video);
            videoComment.setComments(comments);

            code = 200;
        }

        return new DataResult(code, "", videoComment);
    }

    /**
     * 获取视频列表
     *
     * @return 视频列表
     */
    @Override
    public Result getVideoList() {

        // 返回类型
        @Data
        @AllArgsConstructor
        class Response {
            @JsonProperty("video_bid")
            private String videoBvid;
            @JsonProperty("video_title")
            private String videoTitle;
            @JsonProperty("operation_time")
            private LocalDateTime videoSavedate;
        }

        List<Video> videos = videoMapper.selectAll();

        // 按返回格式要求进行包装
        List<Response> responses = new ArrayList<>();
        for (Video video : videos) {
            responses.add(new Response(video.getVideoBvid(), video.getVideoTitle(), video.getVideoSavedate()));
        }
        Map<String, Object> map = new HashMap<>();
        map.put("videos", responses);

        return new DataResult(200, "", map);
    }

    /**
     * 获取视频总体分析数据
     * 待测试
     *
     * @param bv 视频bv号
     * @return 分析结果
     * 结果格式为两个列表，一个是情感分析结果，一个是情感分析结果对应的评论数
     */
    @Override
    public Result getVideoStatisticsOverview(String bv) {
        // 获取视频信息
        List<Comment> comments = commentMapper.selectAllByVideoBvid(bv);

        // 若没有评论则返回
        if (comments == null || comments.size() == 0) {
            return new DataResult(407, "", null);
        }

        // 提取情感分析结果
        ArrayList<String> emotions = new ArrayList<>();
        for (Comment comment : comments) {
            emotions.add(comment.getCommentEmotion());
        }

        // 统计情感分析结果
        Map<String, Integer> map = Tool.getPerItemNum(emotions);

        ArrayList<String> keys = new ArrayList<>();
        ArrayList<Integer> values = new ArrayList<>();

        map.forEach((k, v) -> {
            keys.add(k);
            values.add(v);
        });

        // 将结果整合起来
        Map<String, Object> result = new HashMap<>();
        result.put("emotion", keys);
        result.put("num_person", values);

        // 返回结果
        return new DataResult(200, "", result);
    }

    /**
     * 获取视频IP的统计信息
     * 返回结果包括以下几个部分：
     * 1. 所有存在的情感
     * 1.1 每个情感的IP集合
     * 1.2 每个情感的IP集合对应的评论数
     * 2. 所有存在的IP
     * 2.1 每个IP的情感集合
     * 2.2 每个IP的情感集合对应的评论数
     * 3. 所有IP对应的人数
     *
     * @param bv 视频bv号
     * @return 分析结果
     */
    @Override
    public Result getVideoIpOverview(String bv) {
        List<Comment> comments = commentMapper.selectAllByVideoBvid(bv);
        if (comments == null || comments.size() == 0) {
            return new DataResult(407, "", null);
        }

        // 情感-IP-评论数
        Map<String, Map<String, Integer>> emotionMap = new HashMap<>();
        // IP-情感-评论数
        Map<String, Map<String, Integer>> ipMap = new HashMap<>();

        for (Comment comment : comments) {
            String emotion = comment.getCommentEmotion();
            String ip = comment.getUserIp();

            // 情感-IP-评论数
            Map<String, Integer> emotionSubMap = emotionMap.computeIfAbsent(emotion, k -> new HashMap<>());
            int num = emotionSubMap.getOrDefault(ip, 0);
            emotionSubMap.put(ip, num + 1);

            // IP-情感-评论数
            Map<String, Integer> ipSubMap = ipMap.computeIfAbsent(ip, k -> new HashMap<>());
            num = ipSubMap.getOrDefault(emotion, 0);
            ipSubMap.put(emotion, num + 1);
        }

        // 按照要求整合结果
        ArrayList<String> emotions = new ArrayList<>();
        ArrayList<ArrayList<String>> emotionIp = new ArrayList<>();
        ArrayList<ArrayList<Integer>> emotionIpNum = new ArrayList<>();
        emotionMap.forEach((k, v) -> {
            emotions.add(k);
            ArrayList<String> ips = new ArrayList<>();
            ArrayList<Integer> nums = new ArrayList<>();
            v.forEach((k1, v1) -> {
                ips.add(k1);
                nums.add(v1);
            });
            emotionIp.add(ips);
            emotionIpNum.add(nums);
        });

        ArrayList<String> ips = new ArrayList<>();
        ArrayList<ArrayList<String>> ipEmotion = new ArrayList<>();
        ArrayList<ArrayList<Integer>> ipEmotionNum = new ArrayList<>();
        ArrayList<Integer> ipNum = new ArrayList<>();
        ipMap.forEach((k, v) -> {
            ips.add(k);
            ArrayList<String> subEmotions = new ArrayList<>();
            ArrayList<Integer> nums = new ArrayList<>();
            v.forEach((k1, v1) -> {
                subEmotions.add(k1);
                nums.add(v1);
            });
            ipEmotion.add(subEmotions);
            ipEmotionNum.add(nums);

            ipNum.add(nums.stream().mapToInt(Integer::intValue).sum());
        });

        // 封装结果
        Map<String, Object> result = new HashMap<>();
        result.put("emotion", emotions);
        Map<String, Object> emotionResult = new HashMap<>();
        emotionResult.put("ip", emotionIp);
        emotionResult.put("num_ip", emotionIpNum);
        result.put("ip_ratio_per_emotion", emotionResult);

        result.put("ip", ips);
        Map<String, Object> ipResult = new HashMap<>();
        ipResult.put("emotion", ipEmotion);
        ipResult.put("num_emotion", ipEmotionNum);
        result.put("emotion_ratio_per_ip", ipResult);

        result.put("num_ip_person", ipNum);

        return new DataResult(200, "", result);
    }

    /**
     * 批量插入评论
     * 存在两种使用方法
     * 1.未确定分批大小时，默认为80
     * 2.确定分批大小时，传入分批大小
     *
     * @param comments 评论集合
     */
    private void batchInsertComments(List<Comment> comments, int batchSize) {
        for (int i = 0; i < comments.size(); i += batchSize) {
            int endIndex = Math.min(i + batchSize, comments.size());
            List<Comment> subList = comments.subList(i, endIndex);
            commentMapper.addComments(subList);
        }
    }

    private void batchInsertComments(List<Comment> comments) {
        batchInsertComments(comments, 80);
    }
}
