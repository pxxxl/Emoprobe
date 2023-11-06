package com.minjer.controller;

import com.minjer.pojo.Result;
import com.minjer.pojo.VideoComment;
import com.minjer.service.VideoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TestController {
    @Autowired
    private VideoService videoService;

    @RequestMapping(value = "/test")
    public Result test() {
        return videoService.getVideoInfo("BV1Dd4y1B7uP", 0);
    }
}
