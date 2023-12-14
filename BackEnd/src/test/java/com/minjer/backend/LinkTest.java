package com.minjer.backend;

import com.minjer.link.Crawler;
import com.minjer.link.EmotionModule;
import com.minjer.mapper.CommentMapper;
import com.minjer.mapper.VideoMapper;
import com.minjer.pojo.Comment;
import com.minjer.pojo.VideoComment;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.ArrayList;
import java.util.List;

@SpringBootTest
public class LinkTest {
    @Autowired
    private VideoMapper videoMapper;
    @Autowired
    private CommentMapper commentMapper;

    @Test
    /**
     * 测试爬虫
     * 单独测试和爬虫的链接，测试爬虫是否能够正常爬取视频信息
     * 不涉及数据库
     */
    void crawlerTest() {
        VideoComment videoComment = Crawler.getVideoWithComments("BV1ag4y1Q7iB");
        System.out.println(videoComment);

    }

    @Test
    /**
     * 测试爬虫
     * 测试爬虫是否能够正常爬取视频信息
     * 同时将爬取到的信息存入数据库
     * 目前存在的问题：
     * 1.爬取到的评论信息中存在emoji表情，无法存入数据库
     * 2.可能存在分表需求，导致sql语句过长
     */
    void addVideoTest() {
        String bv = "BV1hH4y1z7c9";
        videoMapper.delByVideoBvid(bv);
        VideoComment videoComment = Crawler.getVideoWithComments(bv);
        System.out.println(videoComment.getVideo());
        videoMapper.addVideo(videoComment.getVideo());
//        List comments = videoComment.obtainCommentTexts();
//        for (int i = 0; i < comments.size(); i++) {
//            System.out.println(i + ": " + comments.get(i));
//        }

        int batchSize = 80; // 子列表的大小
        List<Comment> originalList = videoComment.getComments();

        for (int i = 0; i < originalList.size(); i += batchSize) {
            int endIndex = Math.min(i + batchSize, originalList.size());
            List<Comment> sublist = originalList.subList(i, endIndex);
            commentMapper.addComments(sublist);

        }
    }

    @Test
    /**
     * 测试情感分析模块
     * 测试情感分析模块是否能够正常分析情感
     * 只测试分析模块这一个部分，不涉及爬虫和数据库
     */
    void EmotionModuleTset() {
        List<String> list = new ArrayList<>();
        for (int i = 0; i < 100; i++) {
            list.add("测试消息" + i);
        }
        System.out.println(EmotionModule.handleSentenceInFile("D:\\Java\\code\\Emoprobe\\DeepLearning\\example.json"));
    }
}
