package com.minjer.exception;

import com.minjer.pojo.Result;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

/**
 * 全局异常处理器
 *
 * @author Minjer
 */
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(Exception.class)
    public Result handleException(Exception e) {
        log.error("handleException: ", e);
        log.error("handleException: " + e.getMessage());
        return new Result(500, "服务器出现异常，请联系管理员");
    }
}
