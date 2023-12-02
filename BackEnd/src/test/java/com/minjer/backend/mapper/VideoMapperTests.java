package com.minjer.backend.mapper;


import com.minjer.mapper.VideoMapper;
import com.minjer.pojo.Video;
import com.minjer.utils.Tool;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;

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
        video.setVideoBvid("uhdkw");
        videoMapper.addVideo(video);
    }

    @Test
    void delByBvid() {
        System.out.println(videoMapper.delByVideoBvid("hgwiddudq"));
    }

    @Test
    void toolTest(){
        ArrayList<Integer> list = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            for (int i1 = 0; i1 <= i; i1++) {
                list.add(i);
            }
        }
        System.out.println(Tool.getPerItemNum(list));
    }
}
