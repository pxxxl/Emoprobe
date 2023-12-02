package com.minjer.mapper;

import com.minjer.pojo.Comment;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.logging.log4j.util.Strings;

import java.time.LocalDateTime;
import java.util.List;

/**
 * 评论的数据库操作
 */
@Mapper
public interface CommentMapper {
    /**
     * 批量添加评论进数据库
     *
     * @param comments 评论列表
     */
    public void addComments(List<Comment> comments);

    /**
     * 查询所有评论
     *
     * @return 符合条件的评论列表
     */
    public List<Comment> selectAllComments();

    /**
     * 按照bv号查询所有评论
     *
     * @param bv bv号
     * @return 符合条件的评论列表
     */
    public List<Comment> selectAllByVideoBvid(String bv);

    /**
     * 按照评论id查找评论信息
     *
     * @param id 评论id
     * @return 符合条件的评论
     */
    public Comment selectByCommentId(int id);

    /**
     * 按照过滤条件筛选评论
     *
     * @param bv         被筛选的bv号
     * @param ip         被筛选的ip范围，用","分隔
     * @param sex        被筛选的性别范围，用","分隔
     * @param startTime  被筛选的起始时间
     * @param endTime    被筛选的结束时间
     * @param startLike  被筛选的起始点赞数
     * @param endLike    被筛选的结束点赞数
     * @param startReply 被筛选的起始回复数
     * @param endReply   被筛选的结束回复数
     * @param emotion    被筛选的情感范围，用","分隔
     * @return 符合条件的评论列表
     */
    public List<Comment> selectByFilter(
            String bv,
            String ip,
            String sex,
            LocalDateTime startTime,
            LocalDateTime endTime,
            Integer startLike,
            Integer endLike,
            Integer startReply,
            Integer endReply,
            String emotion
    );
}
