package com.minjer.pojo;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * 视频的实体类
 * @author Minjer
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Video {
    @JsonProperty("video_bid")
    private String videoBvid;
    @JsonProperty("video_aid")
    private String videoAid;
    @JsonProperty("owner_uid")
    private String ownerUid;
    @JsonProperty("owner_name")
    private String ownerName;
    @JsonProperty("video_title")
    private String videoTitle;
    @JsonProperty("video_partition")
    private String videoPartition;
    @JsonProperty("video_tables")
    private String videoTables;
    @JsonProperty("video_pubdate")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime videoPubdate;
    @JsonProperty("video_duration")
    private Integer videoDuration;
    @JsonProperty("video_like")
    private Integer videoLike;
    @JsonProperty("video_coin")
    private Integer videoCoin;
    @JsonProperty("video_favorite")
    private Integer videoFavorite;
    @JsonProperty("video_share")
    private Integer videoShare;
    @JsonProperty("video_reply")
    private Integer videoReply;
    @JsonProperty("video_dislike")
    private Integer videoDislike;
    @JsonProperty("video_cid")
    private String videoCid;
    @JsonProperty("operation_time")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime videoSavedate;
}
