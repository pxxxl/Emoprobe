package com.minjer.pojo;

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
    private Integer code;
    private String message;

    public static Result success(){
        return new Result(200,"");
    }

    public static Result success(String message){
        return new Result(200,message);
    }
}
