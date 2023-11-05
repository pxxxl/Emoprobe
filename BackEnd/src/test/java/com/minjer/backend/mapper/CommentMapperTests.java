package com.minjer.backend.mapper;

import com.minjer.mapper.CommentMapper;
import com.minjer.pojo.Comment;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.ArrayList;
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
        commentMapper.selectAllByVideoBvid("hgwiudq");
    }

}
