import numpy as np
import jieba


def load_data():
    """
    load text and label for training
    """
    text_data = []
    with open('dataset/word.txt', 'r', encoding='utf-8') as f:
        for line in f:
            text_data.append(line.strip('\n').split(' '))
    label = np.load('dataset/label.npy')
    return text_data, label


def get_batch(text_data, w2v_model, indices, in_dim):
    """
    get a batch of input

    :param text_data: All word
    :param w2v_model: The word to vector model that is used.
    :param indices: The index that were chosen
    :param in_dim: the input dim of TESAN

    :return: a numpy array that represent word vector.
    """
    batch_size = len(indices)
    # text_length is used to store the length of each sentence
    text_length = []
    for idx in indices:
        text_length.append(len(text_data[idx]))
    # batch_x is a 2-d array that store the word vector of a batch of sentences
    # Its length is the size of batch, and width is the maximum length of the sentences
    batch_x = np.zeros((batch_size, max(text_length), in_dim), dtype=np.float32)

    # Store the word vector into batch_x
    for i, idx in enumerate(indices, 0):
        for j, word in enumerate(text_data[idx], 0):
            try:
                batch_x[i][j] = w2v_model[word]
            except KeyError:
                batch_x[i][j] = w2v_model['。']
    return batch_x


def make_mask(text_data, indices, sent_length):
    """
    Create mask to mark the valid part of each sentence, and mask the part that has no word.
    The valid part will be filled with zero, and invalid part will be filled with -inf

    :param text_data: All word
    :param indices: The index that were chosen
    :param sent_length: the maximum length of the sentences
    """
    batch_size = len(indices)
    text_length = [len(text_data[idx]) for idx in indices]
    # default filled with -inf
    mask = np.full((batch_size, sent_length, 1), float('-inf'), dtype=np.float32)
    # filled with zero
    for i in range(batch_size):
        mask[i][0:text_length[i]] = 0.0
    return mask


def create_word_bag(sentences, vocab):
    """
    Create word bag for given sentences by model vocab

    :param sentences: the input sentences
    :param vocab: word to vector model

    :return: the word bag
    """
    new_word_bag = np.zeros((len(sentences), len(vocab)), dtype=int)
    for i in range(len(sentences)):
        for word in sentences[i]:
            if word in vocab:
                np_vocab = np.array(list(vocab))
                index = np.where(np_vocab == word)[0][0]  # 获取词汇在词汇表中的索引
                new_word_bag[i][index] = 1  # 将词汇在词袋中的对应位置设为1

    return new_word_bag
