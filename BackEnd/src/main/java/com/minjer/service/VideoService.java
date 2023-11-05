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


    /**
     * 从数据库删除视频
     *
     * @param bv
     * @return 消息码
     * 200 成功
     * 407 数据库中不存在该视频
     */
    public int deleteVideo(String bv);

    /**
     * 更新视频信息
     *
     * @param bv
     * @return 消息码
     * 200 成功
     * 407 数据库中不存在该视频
     */
    public int updateVideo(String bv);
}
