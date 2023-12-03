package com.minjer.service.impl;

import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import com.minjer.link.Crawler;
import com.minjer.link.EmotionModule;
import com.minjer.mapper.CommentMapper;
import com.minjer.mapper.VideoMapper;
import com.minjer.pojo.*;
import com.minjer.service.CommentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.RequestBody;

import java.rmi.MarshalledObject;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class CommenntServiceImpl implements CommentService {
    @Autowired
    private CommentMapper commentMapper;
    @Autowired
    private VideoMapper videoMapper;

    /**
     * 感知用户上传的视频评论
     * 待接入测试
     * 业务逻辑：
     * 1.设置视频保存时间
     * 2.调用情感分析API
     * 3.将结果存入数据库
     * 4.返回结果
     * 5.若情感分析API返回null，则返回409，说明情感分析API出错
     *
     * @param videoComment 用户上传的视频评论信息
     * @return 被添加的视频信息
     */
    @Override
    public Result handleComments(VideoComment videoComment) {
        videoComment.getVideo().setVideoSavedate(LocalDateTime.now());
        List<String> emotions = EmotionModule.handleSentence(videoComment.obtainCommentTexts());
        if (emotions.size() != 0) {
            String bv = videoComment.getVideo().getVideoBvid();
            for (int i = 0; i < videoComment.getComments().size(); i++) {
                videoComment.getComments().get(i).setCommentEmotion(emotions.get(i));
                videoComment.getComments().get(i).setVideoBvid(bv);
            }

            videoMapper.addVideo(videoComment.getVideo());
            batchInsertComments(videoComment.getComments());

            Map<String, Object> result = new HashMap<>();
            result.put("video", videoComment.getVideo());

            return new DataResult(200, "", result);
        } else {
            return new DataResult(409, "", null);
        }
    }

    /**
     * 筛选视频评论
     * 待测试
     *
     * @param filter 筛选条件集合
     * @return 含数据的结果
     */
    @Override
    public Result filterComments(Filter filter) {
        // 判断是否存在该视频
        if (videoMapper.selectByBv(filter.getBv()) == null) {
            if (filter.getAutopost() == 1) {
                // 不存在该视频，且自动爬取
                VideoComment withComments = Crawler.getVideoWithComments(filter.getBv());
                if (withComments != null) {
                    // 爬虫成功,将视频信息和评论信息存入数据库
                    videoMapper.addVideo(withComments.getVideo());
                    batchInsertComments(withComments.getComments());
                } else {
                    // 爬虫出错
                    return new DataResult(408, "", null);
                }
            } else {
                // 不存在该视频，且不自动爬取
                return new DataResult(407, "", null);
            }
        }

        // 数据库查询出视频信息
        Video video = videoMapper.selectByBv(filter.getBv());
        List<Comment> comments = null;
        Integer pageNum = 1;
        if (filter.getCommentNum() == 0) {
            // 不进行分页查询
            comments = commentMapper.selectByFilter(
                    filter.getBv(),
                    filter.getIp(),
                    filter.getSex(),
                    filter.splitStartTime(),
                    filter.splitEndTime(),
                    filter.splitStartLike(),
                    filter.splitEndLike(),
                    filter.splitStartReply(),
                    filter.splitEndReply(),
                    filter.getEmotion()
            );
        } else {
            // 进行分页查询
            PageHelper.startPage(filter.getPageIndex() + 1, filter.getCommentNum());
            comments = commentMapper.selectByFilter(
                    filter.getBv(),
                    filter.getIp(),
                    filter.getSex(),
                    filter.splitStartTime(),
                    filter.splitEndTime(),
                    filter.splitStartLike(),
                    filter.splitEndLike(),
                    filter.splitStartReply(),
                    filter.splitEndReply(),
                    filter.getEmotion()
            );
            PageInfo<Comment> pageInfo = new PageInfo<>(comments);
            pageNum = pageInfo.getPages();
        }
        Map<String, Object> map = Map.of(
                "video", video,
                "comments", comments,
                "total_page_num", pageNum
        );
        return new DataResult(200, "", map);
    }

    /**
     * 批量插入评论
     *
     * @param comments 评论集合
     */
    private void batchInsertComments(List<Comment> comments, int batchSize) {
        for (int i = 0; i < comments.size(); i += batchSize) {
            int endIndex = Math.min(i + batchSize, comments.size());
            List<Comment> subList = comments.subList(i, endIndex);
            commentMapper.addComments(subList);
        }
    }
    private void batchInsertComments(List<Comment> comments) {
        batchInsertComments(comments, 80);
    }

}
