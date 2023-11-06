package com.minjer.pojo;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * @author Minjer
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Sentence {
    @JsonProperty("content")
    private String sentenceText;
    @JsonProperty("emotion")
    private String sentenceEmotion;
}
