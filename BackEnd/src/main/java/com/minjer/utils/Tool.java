package com.minjer.utils;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Tool {
    public static Map<String,Integer> getPerItemNum(List list){
        if (list == null || list.size() == 0){
            return new HashMap<>(0);
        }
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

    /**
     * 将json字符串保存到文件
     * @param json json字符串
     * @param path 保存路径
     */
    public static void saveJsonToFile(String json, String path) {
        String fileName = path + File.separator +"emotion_temp.json";

        try (BufferedWriter writer = new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(fileName), StandardCharsets.UTF_8))) {
            writer.write(json);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
