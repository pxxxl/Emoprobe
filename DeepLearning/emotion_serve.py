"""
## 网络HTTP调用

> /api/emotion

*请求方式：POST
**正文参数：**

(无)

附带信息：
根对象：
| 字段    | 类型 | 内容     | 备注                          |
| ------- | ---- | -------- | ----------------------------- |
| comments | list  | 评论字符串列表 |                       |

其中，comments是字符串类型的列表，每一个字符串代表一条评论。


**效果**

将返回结果字符串，字符串以json格式组织，内容如下。

**json回复：**
根对象：
| 字段    | 类型 | 内容     | 备注                          |
| ------- | ---- | -------- | ----------------------------- |
| code | num  | 程序运行是否正确 |  如果成功返回，code是0，否则是1                     |
| msg | str  | 错误信息 | 如果发生错误，msg会记录错误信息                      |
| comments | list  | 评论字符串列表 |                       |
| emotions    | list  | 情绪字符串列表   |   |
"""

"""
REFERENCE:
import argparse
import os
import json
import jieba
import torch
import numpy as np
import pickle
import logging
from typing import *
from common.utils import get_batch, make_mask, create_word_bag

MAX_COMMENTS = 10


def inf(comments: str, w2v_model, net, vocab, device) -> List[str]:
    IN_DIM = 300
    mood_dict = {
        0: '快乐',
        1: '愤怒',
        2: '厌恶',
        3: '恐惧',
        4: '悲伤',
        5: '惊讶'
    }
    index = []
    segmented_comments = []
    for i in range(len(comments)):
        index.append(i)
        segmented_comment = list(jieba.cut(comments[i]))
        segmented_comments.append(segmented_comment)

    with torch.no_grad():
        batch_x = torch.from_numpy(get_batch(segmented_comments, w2v_model, index, IN_DIM)).float().to(device)
        batch_mask = torch.from_numpy(make_mask(segmented_comments, index, batch_x.shape[1])).float().to(device)
        new_word_bag = torch.from_numpy(create_word_bag(segmented_comments, vocab)).float().to(device)
    net.eval()
    _, out = net(new_word_bag, batch_x, batch_mask, compute_loss=False)

    _, mood = torch.max(out, dim=1)
    mood_list = mood.tolist()
    mood_list = [mood_dict[mood] for mood in mood_list]
    return mood_list


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
    device = torch.device('cuda'if torch.cuda.is_available() else 'cpu')
    jieba.setLogLevel(logging.INFO)

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

    # pbar = tqdm.tqdm(range(0, len(comments), MAX_COMMENTS))

    emotions = []
    batch_num = len(comments) // MAX_COMMENTS
    current_folder_path = os.path.dirname(os.path.abspath(__file__))

    w2v_model = pickle.load(open(os.path.join(current_folder_path, 'model/sgns.weibo.pickle'), 'rb'))
    net = torch.load(os.path.join(current_folder_path, 'model/model.pkl'),  map_location=device)

    vocab = np.load(os.path.join(current_folder_path,'model/vocab.npy'), allow_pickle=True)
    for i in range(0, len(comments), MAX_COMMENTS):
        emotions += inf(comments[i:i + MAX_COMMENTS], w2v_model, net, vocab, device)
        # pbar.set_description(f"Processing batch {i// MAX_COMMENTS+1}/{len(comments) // MAX_COMMENTS}")
        # pbar.update()
    if len(comments) % MAX_COMMENTS != 0 and len(comments) > MAX_COMMENTS:
        emotions += inf(comments[batch_num * MAX_COMMENTS:], w2v_model, net, vocab, device)
    # pbar.close()
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

"""

from flask import Flask, request, jsonify
import argparse
import os
import json
import jieba
import torch
import numpy as np
import pickle
import logging
from typing import *
from common.utils import get_batch, make_mask, create_word_bag

MAX_COMMENTS = 10

def inf(comments: str, w2v_model, net, vocab, device) -> List[str]:
    IN_DIM = 300
    mood_dict = {
        0: '快乐',
        1: '愤怒',
        2: '厌恶',
        3: '恐惧',
        4: '悲伤',
        5: '惊讶'
    }
    index = []
    segmented_comments = []
    for i in range(len(comments)):
        index.append(i)
        segmented_comment = list(jieba.cut(comments[i]))
        segmented_comments.append(segmented_comment)

    with torch.no_grad():
        batch_x = torch.from_numpy(get_batch(segmented_comments, w2v_model, index, IN_DIM)).float().to(device)
        batch_mask = torch.from_numpy(make_mask(segmented_comments, index, batch_x.shape[1])).float().to(device)
        new_word_bag = torch.from_numpy(create_word_bag(segmented_comments, vocab)).float().to(device)
    net.eval()
    _, out = net(new_word_bag, batch_x, batch_mask, compute_loss=False)

    _, mood = torch.max(out, dim=1)
    mood_list = mood.tolist()
    mood_list = [mood_dict[mood] for mood in mood_list]
    return mood_list


def get_error_json_string() -> str:
    result_dict = {
        "code": 1,
        'msg': 'An error occurred.',
        'comments': None,
        'emotions': None
    }
    result_json_string = json.dumps(result_dict)
    return result_json_string


app = Flask(__name__)

@app.route('/api/emotion', methods=['POST'])
def emotion():
    device = torch.device('cuda'if torch.cuda.is_available() else 'cpu')
    jieba.setLogLevel(logging.INFO)

    if request.method == 'POST':
        try:
            comments = request.json['comments']
        except json.JSONDecodeError:
            return get_error_json_string()

    emotions = []
    batch_num = len(comments) // MAX_COMMENTS
    current_folder_path = os.path.dirname(os.path.abspath(__file__))

    w2v_model = pickle.load(open(os.path.join(current_folder_path, 'model/sgns.weibo.pickle'), 'rb'))
    net = torch.load(os.path.join(current_folder_path, 'model/model.pkl'),  map_location=device)

    vocab = np.load(os.path.join(current_folder_path,'model/vocab.npy'), allow_pickle=True)
    for i in range(0, len(comments), MAX_COMMENTS):
        emotions += inf(comments[i:i + MAX_COMMENTS], w2v_model, net, vocab, device)
    if len(comments) % MAX_COMMENTS != 0 and len(comments) > MAX_COMMENTS:
        emotions += inf(comments[batch_num * MAX_COMMENTS:], w2v_model, net, vocab, device)
    result = {'emotions': emotions, 'comments': comments}
    result_json = json.dumps(result)
    return result_json


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

# curl -X POST -H "Content-Type: application/json" -d '{"comments":["value1", "value2"]}' "http://localhost:5001/api/emotion"