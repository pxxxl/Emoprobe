package com.minjer.service;

public interface VideoService {
    /**
     * 添加视频信息进入数据库
     *
     * @param bv
     * @return 消息码
     * 200 成功
     * 405 数据库中已存在该视频
     * 406 出现错误
     */
    public int addVideo(String bv);
}
