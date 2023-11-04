package com.minjer.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
public class DataResult extends Result {
    private Object data;

    public DataResult(int code, String message, Object data) {
        super(code,message);
        this.data = data;
    }


    public static DataResult success(Object data) {
        return new DataResult(200, "", data);
    }

}
