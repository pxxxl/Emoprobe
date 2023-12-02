package com.minjer.utils;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Tool {
    public static Map<String,Integer> getPerItemNum(List list){
        Map<String,Integer> map = new HashMap<>();
        for (Object o : list) {
            String key = o.toString();
            if (map.containsKey(key)){
                map.put(key,map.get(key)+1);
            }else {
                map.put(key,1);
            }
        }
        return map;
    }
}
