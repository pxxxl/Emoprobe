import numpy as np
import os
import jieba


def csv_divider(csv_file):
    # 1. 读取CSV文件，提取标签和中文字符串
    labels = []  # 用于存储标签
    sentences = []  # 用于存储中文字符串
    tag = [0, 1, 2, 3, 4, 5]

    with open(csv_file, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip( ).split(',')
            if len(parts) >= 2:
                if not int(parts[0]) in tag:
                    print('出现错误标签！')
                    continue
                label = int(parts[0])  # 提取标签（第一个字符）
                chinese_text = parts[1]  # 提取中文字符串
                labels.append(label)
                sentences.append(chinese_text)

    # 2. 对标签进行独热编码并存储为 label.npy
    num_samples = len(labels)
    one_hot_labels = np.zeros((num_samples, 6))

    for i, label in enumerate(labels):
        one_hot_labels[i, label] = 1

    np.save('../dataset/label.npy', one_hot_labels)

    # 3. 对中文字符串进行分词并保存到 word.txt
    with open('../dataset/word.txt', 'w', encoding='utf-8') as word_file:
        for sentence in sentences:
            words = jieba.cut(sentence)  # 使用jieba进行分词
            word_file.write(' '.join(words) + '\n')

    print('Label and word files created successfully.')


def create_word_bag():
    with open('../dataset/word.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 构建词汇表
    vocab = set()
    for line in lines:
        words = line.strip().split()
        vocab.update(words)

    # 创建词袋表示的空数组
    word_bag = np.zeros((len(lines), len(vocab)), dtype=int)

    # 填充词袋表示
    for i, line in enumerate(lines):
        words = line.strip( ).split( )
        for word in words:
            if word in vocab:
                word_bag[i, list(vocab).index(word)] = 1

    np.save('../dataset/vocab.npy', vocab)
    np.save('../dataset/word_bag.npy', word_bag)


csv_file = os.path.join('raw_data', 'tagged_sentences.csv')
csv_divider(csv_file)
create_word_bag()