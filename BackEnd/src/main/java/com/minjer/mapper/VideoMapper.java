package com.minjer.mapper;

import com.minjer.pojo.Video;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

/**
 * 视频信息的数据库操作
 */
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
     * @return 删除的行数
     */
    public int delByVideoBvid(String bv);

    /**
     * 获取所有视频
     * @return 所有视频
     */
    public List<Video> selectAll();
}
