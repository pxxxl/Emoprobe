package com.minjer.service;

import com.minjer.pojo.Result;
import com.minjer.pojo.VideoComment;

public interface CommentService {
    /**
     * 感知由用户上传的评论信息
     * @param videoComment 用户上传的视频评论信息
     * @return 进行完情感分析的结果
     */
    public Result handleComments(VideoComment videoComment);
}
