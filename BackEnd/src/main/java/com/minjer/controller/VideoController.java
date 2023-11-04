package com.minjer.controller;

import com.minjer.pojo.Result;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

/**
 * @author Minjer
 */
@RestController
public class VideoController {

    /**
     * 添加视频信息进入数据库
     * 未开始
     * @param bv
     * @return
     */
    @RequestMapping(value = "/api/v1/videos", method = RequestMethod.POST)
    public Result addVideo(String bv){
        return Result.success("添加视频信息进入数据库");
    }

    /**
     * 从数据库删除视频
     * 未开始
     * @param bv
     * @return
     */
    @RequestMapping(value = "/api/v1/videos",method = RequestMethod.DELETE)
    public Result deleteVideo(String bv){
        return Result.success("从数据库删除视频");
    }

    /**
     * 更新视频信息
     * 未开始
     * @param bv
     * @return
     */
    @RequestMapping(value = "/api/v1/videos",method = RequestMethod.PUT)
    public Result updateVideo(String bv){
        return Result.success("更新视频信息");
    }


    /**
     * 获取指定视频信息
     * 未开始
     * @param bv 视频bv号
     * @param autopost
     * @return
     */
    @RequestMapping(value = "/api/v1/videos",method = RequestMethod.GET)
    public Result getVideoInfo(String bv, int autopost){
        return Result.success("获取指定视频信息");
    }

    /**
     * 获取视频列表
     * 未开始
     * @return
     */
    @RequestMapping(value = "/api/v1/videos/list",method = RequestMethod.GET)
    public Result getVideos(){
        return Result.success("获取视频列表");
    }

}
