package com.minjer.pojo;

import com.fasterxml.jackson.annotation.JsonFormat;
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
public class Sentence {
    @JsonProperty("content")
    private String sentenceText;
    @JsonProperty("emotion")
    private String sentenceEmotion;
    @JsonProperty("operation_time")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime sentenceSavetime;
}
