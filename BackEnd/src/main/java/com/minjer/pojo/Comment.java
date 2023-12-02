package com.minjer.pojo;

import com.alibaba.fastjson.annotation.JSONField;
import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
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
    @JsonProperty("user_uid")
    private String userId;
    @JsonProperty("user_name")
    private String userName;
    @JsonProperty("user_ip")
    private String userIp;
    @JsonProperty("user_sex")
    private String userSex;
    @JsonProperty("comment_date")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime commentDate;
    @JsonProperty("comment_text")
    private String commentText;
    @JsonProperty("comment_like")
    private Integer commentLike;
    @JsonProperty("comment_reply")
    private Integer commentReply;
    @JsonProperty("emotion")
    private String commentEmotion;
    @JsonIgnore
    private String videoBvid;
}
