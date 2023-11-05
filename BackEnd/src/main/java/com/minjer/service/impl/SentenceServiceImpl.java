package com.minjer.service.impl;

import com.minjer.mapper.SentenceMapper;
import com.minjer.service.SentenceService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class SentenceServiceImpl implements SentenceService {
    @Autowired
    private SentenceMapper sentenceMapper;
}
