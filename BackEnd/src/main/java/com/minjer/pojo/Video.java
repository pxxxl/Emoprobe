package com.minjer.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * @author Minjer
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Video {
    private String videoBvid;
    private String videoAid;
    private String ownerUid;
    private String ownerName;
    private String videoTitle;
    private String videoTables;
    private LocalDateTime videoPubDate;
    private Integer videoDuration;
    private Integer videoLike;
    private Integer videoCoin;
    private Integer videoFavorite;
    private Integer videoShare;
    private Integer videoReply;
    private Integer videoDislike;
    private String videoCid;
    private LocalDateTime videoSaveDate;
}
