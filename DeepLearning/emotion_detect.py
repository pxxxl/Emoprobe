import argparse
import os
import sys
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
    sys.path.append(os.path.abspath('../'))


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
    if len(comments) % MAX_COMMENTS != 0:
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
