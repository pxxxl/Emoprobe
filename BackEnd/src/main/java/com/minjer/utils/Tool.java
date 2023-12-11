package com.minjer.utils;

import java.nio.file.Path;
import java.nio.file.Paths;
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

    /**
     * 获取指定路径的上级路径
     * @param path 指定路径
     * @param levels 上级路径的层数
     * @return 上级路径
     */
    public static String traverseUp(String path, int levels) {
        Path filePath = Paths.get(path).normalize();

        for (int i = 0; i < levels; i++) {
            filePath = filePath.getParent();
            // 如果到达根目录或无法继续向上访问，则返回当前路径
            if (filePath == null) {
                return path;
            }
        }

        return filePath.toString();
    }
}
