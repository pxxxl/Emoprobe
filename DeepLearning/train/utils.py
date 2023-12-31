import numpy as np


def load_data():
    # text
    text_data = []
    with open('dataset/word.txt', 'r', encoding='utf-8') as f:
        for line in f:
            text_data.append(line.strip('\n').split(' '))
    # label
    label = np.load('dataset/label.npy')

    return text_data, label


def get_batch(text_data, w2v_model, indices, in_dim):
    batch_size = len(indices)
    # 一个 list 用来存储每句话的长度
    text_length = []
    for idx in indices:
        text_length.append(len(text_data[idx]))
    # 一个二维数组，存储了一个 batch 的文字信息，长为 batch_size，即 index 的长度，宽为最长那句话的长度
    batch_x = np.zeros((batch_size, max(text_length), in_dim), dtype=np.float32)

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