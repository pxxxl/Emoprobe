package com.minjer.mapper;

import com.minjer.pojo.Sentence;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

/**
 * 评论句子的数据库操作
 */
@Mapper
public interface SentenceMapper {
    /**
     * 批量添加评论句子进数据库
     * @param sentences 评论句子列表
     */
    public void addSentences(List<Sentence> sentences);
}
