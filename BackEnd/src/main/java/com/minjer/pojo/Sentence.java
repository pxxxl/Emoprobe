package com.minjer.pojo;

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
    private String sentenceText;
    private String sentenceEmotion;
}
