package com.minjer.controller;

import com.minjer.pojo.Result;
import com.minjer.pojo.Sentence;
import com.minjer.service.SentenceService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@RestController
public class SentenceController {

    @Autowired
    private SentenceService sentenceService;

    /**
     * 快速感知评论信息
     * 待接入测试
     *
     * @param comments 评论信息
     *                 {
     *                 "comments": [
     *                 "这个视频真的很好看",
     *                 "这个视频真的很难看"
     *                 ]
     *                 }
     * @return 含数据的结果
     */
    @RequestMapping(value = "/api/v1/sentence", method = RequestMethod.POST)
    public Result handleSentences(@RequestBody Map<String, List<String>> comments) {
        ArrayList<String> sentences = (ArrayList<String>) comments.get("comments");
        Result result = sentenceService.handleSentences(sentences);
        return result;
    }
}
