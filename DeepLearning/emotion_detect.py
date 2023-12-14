import argparse
import json
import torch
import numpy as np
import pickle
from torch.autograd import Variable
from typing import *

def try_gpu(i=0):  #@save
    """如果存在，则返回gpu(i)，否则返回cpu()"""
    if torch.cuda.device_count() >= i + 1:
        return torch.device(f'cuda:{i}')
    return torch.device('cpu')


def inf(comments: str) -> List[str]:
    mood_dict = {
        0: '快乐',
        1: '愤怒',
        2: '厌恶',
        3: '恐惧',
        4: '悲伤',
        5: '惊讶'
    }

    def get_batch(text_data, w2v_model, indices):
        batch_size = len(indices)
        # 一个 list 用来存储每句话的长度
        text_length = []
        for idx in indices:
            text_length.append(len(text_data[idx]))
        # 一个二维数组，存储了一个 batch 的文字信息，长为 batch_size，即 indice 的长度，宽为最长那句话的长度
        batch_x = np.zeros((batch_size, max(text_length), 300), dtype=np.float32)

        # 将第 i 句话的第 j 个词的词向量存储在 batch_x 中
        for i, idx in enumerate(indices, 0):
            for j, word in enumerate(text_data[idx], 0):
                try:
                    batch_x[i][j] = w2v_model[word]
                except KeyError:
                    batch_x[i][j] = w2v_model['。']
        # 返回的是 numpy 数组
        return batch_x

    def make_mask(text_data, indices, sent_length):
        batch_size = len(indices)
        text_length = [len(text_data[idx]) for idx in indices]
        # 上面两行和之前的写法其实等效的

        # 填充负无穷
        mask = np.full((batch_size, sent_length, 1), float('-inf'), dtype=np.float32)

        # 创建了掩码，将没有文字的部分掩掉
        for i in range(batch_size):
            mask[i][0:text_length[i]] = 0.0
        return mask

    w2v_model = pickle.load(open('model/sgns.weibo.pickle', 'rb'))
    net = torch.load('model/model.pkl')
    net = net.to(device=try_gpu())

    # 读取词袋

    vocab = np.load('model/vocab.npy', allow_pickle=True)
    vocab = vocab.tolist()

    def create_word_bag(sentences, vocab):
        new_word_bag = np.zeros((len(sentences), len(vocab)), dtype=int)
        for i in range(len(sentences)):
            # 对单个语句进行分词
            words = sentences[i].strip().split()
            # 遍历新语句的每个词汇
            for word in words:
                if word in vocab:
                    np_vocab = np.array(list(vocab))
                    index = np.where(np_vocab == word)[0][0]  # 获取词汇在词汇表中的索引
                    new_word_bag[i][index] = 1  # 将词汇在词袋中的对应位置设为1

        return new_word_bag
    index = []
    for i in range(len(comments)):
        index.append(i)

    new_word_bag = create_word_bag(comments, vocab)

    with torch.no_grad():
        batch_x = get_batch(comments, w2v_model, index)
        batch_x = Variable(torch.from_numpy(batch_x).float())
        batch_x = batch_x.to(device=try_gpu())
        batch_mask = make_mask(comments, index, batch_x.shape[1])
        batch_mask = Variable(torch.from_numpy(batch_mask).float())
        batch_mask = batch_mask.to(device=try_gpu())

        new_word_bag = torch.from_numpy(new_word_bag).float()
        new_word_bag = new_word_bag.to(device=try_gpu())

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

max_comments_batch = 50

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

    # emotions = inf(comments)
    emotions = []
    batch_num = len(comments) // max_comments_batch
    for i in range(0, len(comments), max_comments_batch):
        emotions += inf(comments[i:i + max_comments_batch])
    if len(comments) % max_comments_batch != 0:
        emotions += inf(comments[batch_num * max_comments_batch:])
    

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