package com.minjer.service.impl;

import com.minjer.link.EmotionModule;
import com.minjer.mapper.CommentMapper;
import com.minjer.mapper.VideoMapper;
import com.minjer.pojo.DataResult;
import com.minjer.pojo.Result;
import com.minjer.pojo.VideoComment;
import com.minjer.service.CommentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class CommenntServiceImpl implements CommentService {
    @Autowired
    private CommentMapper commentMapper;
    @Autowired
    private VideoMapper videoMapper;

    /**
     * 快速感知评论信息
     * 待接入测试
     * 业务逻辑：
     * 1.设置视频保存时间
     * 2.调用情感分析API
     * 3.将结果存入数据库
     * 4.返回结果
     * 5.若情感分析API返回null，则返回409，说明情感分析API出错
     *
     * @param videoComment 用户上传的视频评论信息
     * @return 含数据的结果
     */
    @Override
    public Result handleComments(VideoComment videoComment) {
        videoComment.getVideo().setVideoSavedate(LocalDateTime.now());
        List<String> emotions = EmotionModule.handleSentence(videoComment.getCommentTexts());
        if (emotions != null) {
            String bv = videoComment.getVideo().getVideoBvid();
            for (int i = 0; i < videoComment.getComments().size(); i++) {
                videoComment.getComments().get(i).setCommentEmotion(emotions.get(i));
                videoComment.getComments().get(i).setVideoBvid(bv);
            }

            videoMapper.addVideo(videoComment.getVideo());
            commentMapper.addComments(videoComment.getComments());

            return new DataResult(200, "", videoComment);
        } else {
            return new DataResult(409, "", null);
        }
    }
}
