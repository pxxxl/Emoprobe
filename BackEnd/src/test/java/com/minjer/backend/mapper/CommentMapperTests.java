package com.minjer.backend.mapper;

import com.minjer.mapper.CommentMapper;
import com.minjer.pojo.Comment;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@SpringBootTest
public class CommentMapperTests {
    @Autowired
    private CommentMapper commentMapper;

    @Test
    public void selectByCommentId() {
        System.out.println(commentMapper.selectByCommentId(1));
    }

    @Test
    public void addComments() {
        Comment comment = commentMapper.selectByCommentId(1);
        List<Comment> list = new ArrayList<>();
        comment.setVideoBvid("hgwiudq");

        for (int i = 0; i < 10; i++) {
            list.add(comment);
        }

        commentMapper.addComments(list);
    }

    @Test
    public void selectAll() {
        List<Comment> list = commentMapper.selectAllComments();
    }

    @Test
    public void selectByBvid() {

        List<Comment> list = commentMapper.selectAllByVideoBvid("BV1Dd4y1B7uP");
        for (Comment comment : list) {
            System.out.println(comment);
        }
    }

    @Test
    public void selectByFilter() {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        List<Comment> list = commentMapper.selectByFilter("BV1Fu411R7zz", "", null,
                LocalDateTime.parse("2022-02-17 14:19:13", formatter),
                LocalDateTime.parse("2022-02-18 17:59:39", formatter)
                , null, null, null, null, null);
        System.out.println(list);
    }

    @Test
    public void selectByFilter2() {
        String s = ",1";
        String[] split = s.split(",");
        System.out.println(Arrays.toString(split));
        System.out.println("123"+split[0]+"123");
    }
}
