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

    public Filter(String bv) {
        this.bv = bv;
        this.autopost = 0;
        this.commentNum = 0;
        this.pageIndex = 0;
    }

    public LocalDateTime splitStartTime() {
        if (date == null || "".equals(date)) {
            return null;
        }
        String[] dates = date.split(",");
        if ("".equals(dates[0])) {
            return LocalDateTime.parse("1970-01-01 00:00:00");
        }

        return LocalDateTime.parse(dates[0]);
    }

    public LocalDateTime splitEndTime() {
        if (date == null || "".equals(date)) {
            return null;
        }
        String[] dates = date.split(",");
        if (dates.length == 1 || "".equals(dates[1])) {
            return LocalDateTime.parse("2099-12-31 23:59:59");
        }
        return LocalDateTime.parse(dates[1]);
    }

    public Integer splitStartLike() {
        if (like == null || "".equals(like)) {
            return null;
        }

        String[] likes = like.split(",");
        if ("".equals(likes[0])) {
            return 0;
        }
        return Integer.parseInt(likes[0]);
    }

    public Integer splitEndLike() {
        if (like == null || "".equals(like)) {
            return null;
        }
        String[] likes = like.split(",");
        if (likes.length == 1 || "".equals(likes[1])) {
            return Integer.MAX_VALUE;
        }
        return Integer.parseInt(likes[1]);
    }

    public Integer splitStartReply() {
        if (reply == null || "".equals(reply)) {
            return null;
        }
        String[] replies = reply.split(",");
        if ("".equals(replies[0])) {
            return 0;
        }
        return Integer.parseInt(replies[0]);
    }

    public Integer splitEndReply() {
        if (reply == null || "".equals(reply)) {
            return null;
        }
        String[] replies = reply.split(",");
        if (replies.length == 1 || "".equals(replies[1])) {
            return Integer.MAX_VALUE;
        }
        return Integer.parseInt(replies[1]);
    }

}
