package com.minjer.pojo;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 返回结果的实体类
 * @author Minjer
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Result {
    @JsonProperty("code")
    private Integer code;
    @JsonProperty("msg")
    private String message;

    public Result(int code) {
        this.code = code;
        this.message = "";
    }

    /**
     * 成功返回结果
     * @return Result
     */
    public static Result success() {
        return new Result(200, "");
    }

    /**
     * 成功返回结果
     * @param message 提示信息
     * @return Result
     */
    public static Result success(String message) {
        return new Result(200, message);
    }

    /**
     * 只含消息码的快捷方法
     * @param code 消息码
     * @return Result
     */
    public static Result code(int code) {
        return new Result(code);
    }
}
