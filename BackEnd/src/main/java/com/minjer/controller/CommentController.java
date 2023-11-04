package com.minjer.controller;

import com.minjer.pojo.DataResult;
import com.minjer.pojo.Result;
import com.minjer.service.CommentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CommentController {

    @Autowired
    private CommentService commentService;

    /**
     * 感知由用户上传的评论信息
     * 未开始
     *
     * @return
     */
    @RequestMapping(value = "/api/v1/comments", method = RequestMethod.POST)
    public Result addComments() {
        return DataResult.success(1);
    }


}
