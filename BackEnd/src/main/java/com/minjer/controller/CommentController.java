package com.minjer.controller;

import com.minjer.pojo.Result;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CommentController {
    /**
     * 感知由用户上传的评论信息
     * 未开始
     * @return
     */
    @RequestMapping(value = "/api/v1/comments",method = RequestMethod.POST)
    public Result addComments(){
        return Result.success("感知由用户上传的评论信息");
    }


}
