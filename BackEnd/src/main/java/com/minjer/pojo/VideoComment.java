package com.minjer.pojo;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.ArrayList;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class VideoComment {

    @JsonProperty("video")
    private Video video;
    @JsonProperty("comments")
    private List<Comment> comments;

    public List<String> getCommentTexts() {
        List<String> commentTexts = new ArrayList<>();
        for (Comment comment : comments) {
            commentTexts.add(comment.getCommentText());
        }
        return commentTexts;
    }
}
