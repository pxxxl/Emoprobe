package com.minjer.controller;

import com.minjer.pojo.DataResult;
import com.minjer.pojo.Result;
import com.minjer.pojo.VideoComment;
import com.minjer.service.CommentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

/**
 * 对评论的操作
 *
 * @author Minjer
 */
@RestController
public class CommentController {

    @Autowired
    private CommentService commentService;

    /**
     * 感知由用户上传的评论信息
     * 待测试
     *
     * @param videoComment 用户上传的视频评论信息
     * @return 进行完情感分析的结果
     */
    @RequestMapping(value = "/api/v1/comments", method = RequestMethod.POST)
    public Result addComments(VideoComment videoComment) {

        Result result = commentService.handleComments(videoComment);

        return result;
    }


}
