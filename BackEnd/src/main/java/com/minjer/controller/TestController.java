package com.minjer.controller;

import com.minjer.pojo.Result;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 测试控制器
 * 测试接口是否正常
 *
 * @author Minjer
 */
@RestController
public class TestController {

    @RequestMapping(value = "/test")
    public Result test() {
        return new Result(200, "前面的区域，以后再来探索吧！");
    }
}
