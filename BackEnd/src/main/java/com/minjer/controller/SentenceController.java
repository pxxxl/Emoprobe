package com.minjer.controller;

import com.minjer.pojo.Result;
import com.minjer.pojo.Sentence;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;

@RestController
public class SentenceController {
    /**
     * 快速感知评论信息
     * 未开始
     * @param sentences
     * @return
     */
    @RequestMapping(value = "/api/v1/sentence", method = RequestMethod.POST)
    public Result handleSentences(ArrayList<Sentence> sentences) {
        return Result.success("快速感知评论信息");
    }
}
