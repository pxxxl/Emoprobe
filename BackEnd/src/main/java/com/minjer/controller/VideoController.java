package com.minjer.controller;

import com.minjer.pojo.Result;
import com.minjer.service.VideoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

/**
 * 视频控制器
 *
 * @author Minjer
 */
@RestController
public class VideoController {

    @Autowired
    private VideoService videoService;


    /**
     * 添加视频信息进入数据库
     *
     * @param bv 视频bv号
     * @return 不含数据的结果信息
     */
    @RequestMapping(value = "/api/v1/videos", method = RequestMethod.POST)
    public Result addVideo(String bv) {
        int code = videoService.addVideo(bv);
        return Result.code(code);
    }

    /**
     * 从数据库删除视频
     *
     * @param bv 视频bv号
     * @return 不含数据的结果信息
     */
    @RequestMapping(value = "/api/v1/videos", method = RequestMethod.DELETE)
    public Result deleteVideo(String bv) {
        int code = videoService.deleteVideo(bv);
        return Result.code(code);
    }

    /**
     * 更新视频信息
     *
     * @param bv 视频bv号
     * @return 不含数据的结果信息
     */
    @RequestMapping(value = "/api/v1/videos", method = RequestMethod.PUT)
    public Result updateVideo(String bv) {
        int code = videoService.updateVideo(bv);
        return Result.code(code);
    }


    /**
     * 获取指定视频信息
     *
     * @param bv       视频bv号
     * @param autopost 是否会爬取信息
     * @return 含有数据的结果信息
     */
    @RequestMapping(value = "/api/v1/videos", method = RequestMethod.GET)
    public Result getVideoInfo(String bv, int autopost) {

        Result result = videoService.getVideoInfo(bv, autopost);
        return result;
    }

    /**
     * 获取视频列表
     *
     * @return 含有数据的结果信息
     */
    @RequestMapping(value = "/api/v1/videos/list", method = RequestMethod.GET)
    public Result getVideos() {
        Result result = videoService.getVideoList();
        return result;
    }

    /**
     * 统计视频信息
     * 获取视频评论每种情绪的人数占比信息
     *
     * @param bv bv号
     * @return 统计结果
     */
    @RequestMapping(value = "/api/v1/videos/statistics/overview", method = RequestMethod.GET)
    public Result getVideoStatisticsOverview(String bv) {
        Result result = videoService.getVideoStatisticsOverview(bv);
        return result;
    }

    /**
     * 统计视频信息
     * 获取视频评论IP的信息
     *
     * @param bv bv号
     * @return 统计结果
     */
    @RequestMapping(value = "/api/v1/videos/statistics/ip", method = RequestMethod.GET)
    public Result etVideoIpOverview(String bv) {
        Result result = videoService.getVideoIpOverview(bv);
        return result;
    }
}
