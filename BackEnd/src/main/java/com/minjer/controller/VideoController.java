package com.minjer.controller;

import com.minjer.pojo.Result;
import com.minjer.service.VideoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

/**
 * @author Minjer
 */
@RestController
public class VideoController {

    @Autowired
    private VideoService videoService;


    /**
     * 添加视频信息进入数据库
     *
     * @param bv
     * @return 不含数据的结果信息
     */
    @RequestMapping(value = "/api/v1/videos", method = RequestMethod.POST)
    public Result addVideo(String bv) {
        int code = videoService.addVideo(bv);
        return Result.code(code);
    }

    /**
     * 从数据库删除视频
     * 未开始
     *
     * @param bv
     * @return
     */
    @RequestMapping(value = "/api/v1/videos", method = RequestMethod.DELETE)
    public Result deleteVideo(String bv) {
        return Result.success("从数据库删除视频");
    }

    /**
     * 更新视频信息
     * 未开始
     *
     * @param bv
     * @return
     */
    @RequestMapping(value = "/api/v1/videos", method = RequestMethod.PUT)
    public Result updateVideo(String bv) {
        return Result.success("更新视频信息");
    }


    /**
     * 获取指定视频信息
     * 未开始
     *
     * @param bv       视频bv号
     * @param autopost
     * @return
     */
    @RequestMapping(value = "/api/v1/videos", method = RequestMethod.GET)
    public Result getVideoInfo(String bv, int autopost) {
        return Result.success("获取指定视频信息");
    }

    /**
     * 获取视频列表
     * 未开始
     *
     * @return
     */
    @RequestMapping(value = "/api/v1/videos/list", method = RequestMethod.GET)
    public Result getVideos() {
        return Result.success("获取视频列表");
    }

}
