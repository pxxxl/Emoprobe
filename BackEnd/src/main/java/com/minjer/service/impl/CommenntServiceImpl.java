package com.minjer.service.impl;

import com.minjer.mapper.CommentMapper;
import com.minjer.service.CommentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class CommenntServiceImpl implements CommentService {
    @Autowired
    private CommentMapper commentMapper;
}
