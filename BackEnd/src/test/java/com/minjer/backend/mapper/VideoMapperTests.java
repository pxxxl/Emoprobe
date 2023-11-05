package com.minjer.backend.mapper;


import com.minjer.mapper.VideoMapper;
import com.minjer.pojo.Video;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.io.IOException;
import java.io.InputStream;

@SpringBootTest
public class VideoMapperTests {

    @Autowired
    private VideoMapper videoMapper;

    @Test
    void selectByBv() {
        System.out.println(videoMapper.selectByBv("BV1Dd4y1B7uP"));
        System.out.println(videoMapper.selectByBv("BV1Dd"));
    }

    @Test
    void addVideo() {
        Video video = videoMapper.selectByBv("BV1Dd4y1B7uP");
        video.setVideoBvid("hgwiddudq");
        videoMapper.addVideo(video);
    }

    @Test
    void delByBvid() {
        System.out.println(videoMapper.delByVideoBvid("hgwiddudq"));
    }
}
