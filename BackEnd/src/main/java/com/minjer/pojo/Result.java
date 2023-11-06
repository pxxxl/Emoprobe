package com.minjer.pojo;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
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

    public static Result success() {
        return new Result(200, "");
    }

    public static Result success(String message) {
        return new Result(200, message);
    }

    public static Result code(int code) {
        return new Result(code);
    }
}
