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
    void crawlerTest() {
        VideoComment videoComment = Crawler.getVideoWithComments("BV1uv411q7Mv");
        System.out.println(videoComment);
    }

    @Test
    void addVideoTest(){
        VideoComment videoComment = Crawler.getVideoWithComments("BV1uv411q7Mv");
        videoComment.getVideo().setVideoBvid("BV1uv411q7Mv");
        videoMapper.addVideo(videoComment.getVideo());

        commentMapper.addComments(videoComment.getComments());
    }

    @Test
    void EmotionModuleTset(){
        List<String> list = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            list.add("测试消息"+i);
        }
        System.out.println(EmotionModule.handleSentenceInFile("D:\\Java\\code\\Emoprobe\\DeepLearning\\example.json"));
    }
}
