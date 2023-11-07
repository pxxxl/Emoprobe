package com.minjer.mapper;

import com.minjer.pojo.Comment;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

/**
 * 评论的数据库操作
 */
@Mapper
public interface CommentMapper {
    /**
     * 批量添加评论进数据库
     * @param comments 评论列表
     */
    public void addComments(List<Comment> comments);

    /**
     * 查询所有评论
     * @return 符合条件的评论列表
     */
    public List<Comment> selectAllComments();

    /**
     * 按照bv号查询所有评论
     * @param bv bv号
     * @return 符合条件的评论列表
     */
    public List<Comment> selectAllByVideoBvid(String bv);

    /**
     * 按照评论id查找评论信息
     * @param id 评论id
     * @return 符合条件的评论
     */
    public Comment selectByCommentId(int id);
}
