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
public class Comment {
    private String userId;
    private String userName;
    private String userIp;
    private String userSex;
    private LocalDateTime commentDate;
    private String commentText;
    private Integer commentLike;
    private Integer commentReply;
    private String commentEmotion;
    private String videoBvid;
}
