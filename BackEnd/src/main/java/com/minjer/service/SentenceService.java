package com.minjer.service;

import com.minjer.pojo.Result;

import java.util.List;

public interface SentenceService {
    /**
     * 快速感知评论信息
     * @param sentences 评论信息
     * @return 感知结果
     */
    public Result handleSentences(List<String> sentences);
}
