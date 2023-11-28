import argparse
import json
from typing import *
from snownlp import SnowNLP

def inf(comments: str) -> List[str]:
    # 在这里实现情绪感知的逻辑
    # 返回情绪字符串列表
    emotion_list = [str(SnowNLP(comment).sentiments) for comment in comments]
    return emotion_list


def get_error_json_string() -> str:
    result_dict = {
        "code": 1,
        'msg': 'An error occurred.',
        'comments': None,
        'emotions': None
    }
    result_json_string = json.dumps(result_dict)
    return result_json_string


def parse_arguments():
    parser = argparse.ArgumentParser(description='AI情绪感知接口')
    parser.add_argument('-i', metavar='<以json字符串组织的评论列表>', help='读取以json字符串组织的评论列表')
    parser.add_argument('-fi', metavar='<json文件路径>', help='读取指定路径的json文件作为评论列表')
    parser.add_argument('-o', metavar='<文件保存路径>', help='将结果保存到指定路径的文件')

    return parser.parse_args()

def main():
    args = parse_arguments()

    if args.i is None and args.fi is None:
        print(get_error_json_string())
        return

    if args.fi is not None:
        try:
            with open(args.fi, 'r', encoding='utf-8') as file:
                comments = json.load(file)['comments']
        except FileNotFoundError:
            print(get_error_json_string())
            return
        except json.JSONDecodeError:
            print(get_error_json_string())
            return
    else:
        try:
            comments = json.loads(args.i)['comments']
        except json.JSONDecodeError:
            print(get_error_json_string())
            return

    emotions = inf(comments)

    result = {'emotions': emotions, 'comments': comments}
    result_json = json.dumps(result)

    if args.o is not None:
        try:
            with open(args.o, 'w', encoding='utf-8') as file:
                file.write(result_json)
        except IOError:
            print(get_error_json_string())
    else:
        print(result_json)

if __name__ == '__main__':
    main()