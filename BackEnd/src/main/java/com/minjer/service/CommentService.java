package com.minjer.service;

import com.minjer.pojo.Filter;
import com.minjer.pojo.Result;
import com.minjer.pojo.VideoComment;

public interface CommentService {
    /**
     * 感知由用户上传的评论信息
     * @param videoComment 用户上传的视频评论信息
     * @return 进行完情感分析的结果
     */
    public Result handleComments(VideoComment videoComment);

    /**
     * 根据要求对视频评论进行分类筛选
     * @param filter 筛选条件集合
     * @return 筛选结果
     */
    public Result filterComments(Filter filter);
}
