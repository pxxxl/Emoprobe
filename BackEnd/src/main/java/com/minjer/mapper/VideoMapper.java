package com.minjer.mapper;

import com.minjer.pojo.Video;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface VideoMapper {
    /**
     * 根据bv号获取视频信息
     * @param bv bv号
     * @return 符合条件的视频对象
     */
    public Video selectByBv(String bv);

    /**
     * 添加一条视频信息
     * @param video 视频信息
     */
    public void addVideo(Video video);

    /**
     * 根据bv号删除视频，同时会删除comment表中关联的评论
     * @param bv
     */
    public void delByVideoBvid(String bv);
}
