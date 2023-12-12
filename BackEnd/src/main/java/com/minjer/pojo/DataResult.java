package com.minjer.pojo;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

/**
 * 带有数据的返回结果
 * @author Minjer
 */
@Data
public class DataResult extends Result {
    @JsonProperty("data")
    private Object data;

    public DataResult(int code, String message, Object data) {
        super(code, message);
        this.data = data;
    }

    /**
     * 成功返回结果
     * @param data 获取的数据
     * @return DataResult
     */
    public static DataResult success(Object data) {
        return new DataResult(200, "", data);
    }

}
