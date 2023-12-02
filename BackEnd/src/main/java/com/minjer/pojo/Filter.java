package com.minjer.pojo;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;


@Data
@AllArgsConstructor
@NoArgsConstructor
public class Filter {
    @JsonProperty("bv")
    private String bv;
    @JsonProperty("autopost")
    private Integer autopost;
    @JsonProperty("n_per_page")
    private Integer commentNum;
    @JsonProperty("pn")
    private Integer pageIndex;
    @JsonProperty("user_ip")
    private String ip;
    @JsonProperty("user_sex")
    private String sex;
    @JsonProperty("comment_date")
    private String date;
    @JsonProperty("comment_like")
    private String like;
    @JsonProperty("comment_reply")
    private String reply;
    @JsonProperty("emotion")
    private String emotion;

    public Filter(String bv){
        this.bv = bv;
        this.autopost = 0;
        this.commentNum = 0;
        this.pageIndex = 0;
    }

    public LocalDateTime splitStartTime() {
        if (date == null) {
            return null;
        }
        String[] dates = date.split(",");

        return LocalDateTime.parse(dates[0]);
    }
    public LocalDateTime splitEndTime() {
        if (date == null) {
            return null;
        }
        String[] dates = date.split(",");
        return LocalDateTime.parse(dates[1]);
    }

    public Integer splitStartLike() {
        if (like == null) {
            return null;
        }
        String[] likes = like.split(",");
        return Integer.parseInt(likes[0]);
    }

    public Integer splitEndLike() {
        if (like == null) {
            return null;
        }
        String[] likes = like.split(",");
        return Integer.parseInt(likes[1]);
    }

    public Integer splitStartReply() {
        if (reply == null) {
            return null;
        }
        String[] replies = reply.split(",");
        return Integer.parseInt(replies[0]);
    }

    public Integer splitEndReply() {
        if (reply == null) {
            return null;
        }
        String[] replies = reply.split(",");
        return Integer.parseInt(replies[1]);
    }

}
