from flask import Flask, request
import libcrawl
import json
import argparse
import utils


"""
## 网络HTTP调用

> /api/crawl

*请求方式：GET
**正文参数：**

| 参数名  | 类型 | 内容                     | 必要性         | 备注                                 |
| ------- | ---- | ------------------------ | -------------- | ------------------------------------ |
| bv      | str  | 视频bv号                | 必要           |   形式：“BVXXXXXX”             |


**效果：**
爬取视频信息并返回

**json回复：**
根对象：

| 字段    | 类型 | 内容     | 备注                          |
| ------- | ---- | -------- | ----------------------------- |
| code    | num  | 返回值   |  0：成功<br /> 1：失败 |
| msg | str  | 错误信息 | 默认为空字符串                       |
| data | obj  | 爬取结果 | 如果code为1，则data字段将为空对象                       |

data对象：

| 字段            | 类型 | 内容         | 备注                   |
| --------------- | ---- | ------------ | ---------------------- |
| video              | obj  | 视频信息     |        |
| comments       | list  | 评论列表    |                        |

video对象：
| 字段    | 类型 | 内容     | 备注                          |
| ------- | ---- | -------- | ----------------------------- |
| video_bid       | str  | 视频bv号    | 形式：“BVXXXXXX”       |
| video_aid       | str  | 视频aid号    | 字符串，但是是数字                       |
| owner_uid       | str  | UP主用户uid |  字符串，但是是数字                      |
| owner_name      | str  | UP主用户名   |                        |
| video_title     | str  | 视频标题     |                        |
| video_partition | str  | 视频分区     |                        |
| video_tables    | str  | 视频分区     |                        |
| video_pubdate   | str  | 视频发布时间 | 格式为"2023-10-08 12:40:32"       |
| video_duration  | num  | 视频时长     | 单位为秒                |
| video_like      | num  | 点赞数       |                        |
| video_coin      | num  | 投币数       |                        |
| video_favorite  | num  | 收藏数       |                        |
| video_share     | num  | 分享数       |                        |
| video_reply     | num  | 评论数       |                        |
| video_dislike   | num  | 点踩数       |                        |
| video_cid       | str  | 视频cid号    | 字符串，但是是数字       |
| video_disc      | str  | 视频简介     |                         |

comments对象为一列表，其中所有列表项均为以下对象：

| 字段              | 类型 | 内容     | 备注                     |
| ----------------- | ---- | -------- | ------------------------ |
| user_uid          |      |   str       |  字符串，但是是数字                        |
| user_name         |      |   str       |                          |
| user_ip           |      |   str       |                          |
| user_sex          |      |  str        | 有“保密”、“男”、“女”   |
| comment_date      |      |  str        | 示例："2023-10-08 12:40:32" |
| comment_text      |      |  str        |                          |
| comment_like      |      |  num        | 点赞数量                         |
| comment_reply     |      |  num        | 回复数量                         |
"""

"""
REFERENCE:
def main():
    try:
        parser = argparse.ArgumentParser(description='Video Crawler')
        parser.add_argument('-bv', help=r'Video BV number, form "BVXXXXXXX"', required=True)
        parser.add_argument('-o', help='File save path')
        parser.add_argument('-config', help='Config file path')
        parser.add_argument('-p', help='Pure output mode', action='store_true')
        args = parser.parse_args()
    
        bv = args.bv
        output_path = args.o
        config_path = args.config
        pure_output = args.p

        if not config_path:
            config_path = utils.get_default_config_file_path()
        
        cookie = utils.get_cookie(config_path)

        if pure_output:
            result_json_string = libcrawl.get_result_json_string(bv, cookie, True)
        else:
            result_json_string = libcrawl.get_result_json_string(bv, cookie)
    
        if output_path:
            with open(output_path, 'w') as file:
                file.write(result_json_string)
        else:
            print(result_json_string)
        
    except:
        result_json_string = libcrawl.get_error_json_string()
        print(result_json_string)
"""

app = Flask(__name__)

@app.route('/api/crawl', methods=['GET'])
def crawl():
    try:
        bv = request.args.get('bv')
        utils.log('crawl: bv:' + bv)
        result_json_string = libcrawl.get_result_json_string(bv, "")
        return result_json_string
    except:
        result_json_string = libcrawl.get_error_json_string()
        return result_json_string
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
