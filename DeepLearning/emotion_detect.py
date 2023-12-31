import argparse
import json

import jieba
import torch
import numpy as np
import pickle
import tqdm
import time
import logging

from typing import *

from train.utils import get_batch, make_mask, create_word_bag

MAX_COMMENTS = 50

t1 = time.time()
def inf(comments: str) -> List[str]:
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    IN_DIM = 300
    mood_dict = {
        0: '快乐',
        1: '愤怒',
        2: '厌恶',
        3: '恐惧',
        4: '悲伤',
        5: '惊讶'
    }

    w2v_model = pickle.load(open('model/sgns.weibo.pickle', 'rb'))
    net = torch.load('model/model.pkl').to(device)
    vocab = np.load('model/vocab.npy', allow_pickle=True).tolist()

    index = []
    for i in range(len(comments)):
        index.append(i)

    with torch.no_grad():
        batch_x = torch.from_numpy(get_batch(comments, w2v_model, index, IN_DIM)).float().to(device)
        batch_mask = torch.from_numpy(make_mask(comments, index, batch_x.shape[1])).float().to(device)
        new_word_bag = torch.from_numpy(create_word_bag(comments, vocab)).float().to(device)

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
    for i in range(0, len(comments), MAX_COMMENTS):
        emotions += inf(comments[i:i + MAX_COMMENTS])
        # pbar.set_description(f"Processing batch {i// MAX_COMMENTS+1}/{len(comments) // MAX_COMMENTS}")
        # pbar.update()
    if len(comments) % MAX_COMMENTS != 0:
        emotions += inf(comments[batch_num * MAX_COMMENTS:])
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
