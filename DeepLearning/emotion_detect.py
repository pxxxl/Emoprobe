import argparse
import json
from typing import *
from snownlp import SnowNLP

def inf(comments: str) -> List[str]:
    # 在这里实现情绪感知的逻辑
    # 返回情绪字符串列表
    emotion_list = [str(SnowNLP(comment).sentiments) for comment in comments]
    return emotion_list

def parse_arguments():
    parser = argparse.ArgumentParser(description='AI情绪感知接口')
    parser.add_argument('-i', metavar='<以json字符串组织的评论列表>', help='读取以json字符串组织的评论列表')
    parser.add_argument('-fi', metavar='<json文件路径>', help='读取指定路径的json文件作为评论列表')
    parser.add_argument('-o', metavar='<文件保存路径>', help='将结果保存到指定路径的文件')

    return parser.parse_args()

def main():
    args = parse_arguments()

    if args.i is None and args.fi is None:
        print('请提供评论列表')
        return

    if args.fi is not None:
        try:
            with open(args.fi, 'r', encoding='utf-8') as file:
                comments = json.load(file)['comments']
        except FileNotFoundError:
            print('指定的文件路径不存在')
            return
        except json.JSONDecodeError:
            print('无法解析JSON文件')
            return
    else:
        try:
            comments = json.loads(args.i)['comments']
        except json.JSONDecodeError:
            print('无法解析JSON字符串')
            return

    emotions = inf(comments)

    result = {'emotions': emotions, 'comments': comments}
    result_json = json.dumps(result)

    if args.o is not None:
        try:
            with open(args.o, 'w', encoding='utf-8') as file:
                file.write(result_json)
        except IOError:
            print('无法写入文件')
    else:
        print(result_json)

if __name__ == '__main__':
    main()