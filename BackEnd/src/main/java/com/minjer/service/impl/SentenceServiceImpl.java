package com.minjer.service.impl;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.minjer.link.EmotionModule;
import com.minjer.mapper.SentenceMapper;
import com.minjer.pojo.DataResult;
import com.minjer.pojo.Result;
import com.minjer.pojo.Sentence;
import com.minjer.service.SentenceService;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Service
public class SentenceServiceImpl implements SentenceService {
    @Autowired
    private SentenceMapper sentenceMapper;

    /**
     * 快速感知评论信息
     * 待接入测试
     * 业务逻辑：
     * 1. 调用情感分析API
     * 2. 将结果存入数据库
     * 3. 返回结果
     *
     * @param stringList 评论句子列表
     * @return 含数据的结果
     */
    @Override
    public Result handleSentences(List<String> stringList) {
        // API文档规定的返回数据类型
        @Data
        class Response {
            @Data
            @AllArgsConstructor
            class Sentence {
                @JsonProperty("content")
                private String content;
                @JsonProperty("emotion")
                private String emotion;
            }

            @JsonProperty("operation_time")
            private LocalDateTime operationTime;
            @JsonProperty("comments")
            private List<Sentence> sentences;

            public Response(List<com.minjer.pojo.Sentence> sentences) {
                this.operationTime = LocalDateTime.now();
                this.sentences = new ArrayList<>();
                for (com.minjer.pojo.Sentence sentence : sentences) {
                    this.sentences.add(new Sentence(sentence.getSentenceText(), sentence.getSentenceEmotion()));
                }
            }
        }
        // 调用情感分析模块
        List<String> emotions = EmotionModule.handleSentence(stringList);
        if (emotions != null) {
            // 将句子和情感打包
            LocalDateTime now = LocalDateTime.now();
            List<Sentence> sentences = new ArrayList<>();
            for (int i = 0; i < emotions.size(); i++) {
                sentences.add(new Sentence(stringList.get(i), emotions.get(i), now));
            }
            // 将句子插入数据库
            sentenceMapper.addSentences(sentences);

            // 如果成功，返回数据
            return new DataResult(200, "", new Response(sentences));
        } else {
            // 如果失败，返回错误信息
            return new DataResult(409, "", null);
        }
    }
}
