package com.minjer.controller;

import com.minjer.pojo.Result;
import com.minjer.service.VideoService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

/**
 * 视频控制器
 *
 * @author Minjer
 */
@Slf4j
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
        log.info("addVideo: bv={}", bv);
        int code = videoService.addVideo(bv);
        Result result = Result.code(code);
        log.info("addVideo result: " + result.toString());
        return result;
    }

    /**
     * 从数据库删除视频
     *
     * @param bv 视频bv号
     * @return 不含数据的结果信息
     */
    @RequestMapping(value = "/api/v1/videos", method = RequestMethod.DELETE)
    public Result deleteVideo(String bv) {
        log.info("deleteVideo: bv={}", bv);
        int code = videoService.deleteVideo(bv);
        Result result = Result.code(code);
        log.info("deleteVideo result: " + result.toString());
        return result;
    }

    /**
     * 更新视频信息
     *
     * @param bv 视频bv号
     * @return 不含数据的结果信息
     */
    @RequestMapping(value = "/api/v1/videos", method = RequestMethod.PUT)
    public Result updateVideo(String bv) {
        log.info("updateVideo: bv={}", bv);
        int code = videoService.updateVideo(bv);
        Result result = Result.code(code);
        log.info("updateVideo result: " + result.toString());
        return result;
    }


    /**
     * 获取指定视频信息
     *
     * @param bv       视频bv号
     * @param autopost 是否会爬取信息
     * @return 含有数据的结果信息
     */
    @Deprecated
    @RequestMapping(value = "/api/v1/videos", method = RequestMethod.GET)
    public Result getVideoInfo(String bv, int autopost) {
        log.info("getVideoInfo: bv={}, autopost={}", bv, autopost);
        Result result = videoService.getVideoInfo(bv, autopost);
        log.info("getVideoInfo result: " + result.toString());
        return result;
    }

    /**
     * 获取视频列表
     *
     * @return 含有数据的结果信息
     */
    @RequestMapping(value = "/api/v1/videos/list", method = RequestMethod.GET)
    public Result getVideos() {
        log.info("getVideos");
        Result result = videoService.getVideoList();
        log.info("getVideos result: " + result.toString());
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
        log.info("getVideoStatisticsOverview: bv={}", bv);
        Result result = videoService.getVideoStatisticsOverview(bv);
        log.info("getVideoStatisticsOverview: result={}", result);
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
        log.info("getVideoIpOverview: bv={}", bv);
        Result result = videoService.getVideoIpOverview(bv);
        log.info("getVideoIpOverview: result={}", result);
        return result;
    }
}
