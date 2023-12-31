import numpy as np
import jieba
import warnings


def csv_divider(csv_file, num_class):
    """
    Read CSV file and process it.

    :param csv_file: path to csv file
    :param num_class: number of emotion's classes
    """
    labels = []
    sentences = []
    tag = []
    for emo_class in range(num_class):
        tag.append(emo_class)

    with open(csv_file, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) >= 2:
                if not int(parts[0]) in tag:
                    warnings.warn('Error label!')
                    continue
                label = int(parts[0])
                chinese_text = parts[1]
                labels.append(label)
                sentences.append(chinese_text)
            else:
                warnings.warn('Error format')

    # Hot-key code
    num_samples = len(labels)
    one_hot_labels = np.zeros((num_samples, 6))

    for i, label in enumerate(labels):
        one_hot_labels[i, label] = 1

    np.save('dataset/label.npy', one_hot_labels)

    # Divide sentences into word by jieba
    with open('dataset/word.txt', 'w', encoding='utf-8') as word_file:
        for sentence in sentences:
            words = jieba.cut(sentence)
            word_file.write(' '.join(words) + '\n')
    print('Label and word files created successfully.')


def create_word_bag():
    with open('dataset/word.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    vocab = set()
    for line in lines:
        words = line.strip().split()
        vocab.update(words)

    word_bag = np.zeros((len(lines), len(vocab)), dtype=int)

    for i, line in enumerate(lines):
        words = line.strip().split()
        for word in words:
            if word in vocab:
                word_bag[i, list(vocab).index(word)] = 1
    vocab = np.array(list(vocab))
    np.save('../model/vocab.npy', vocab)
    np.save('dataset/word_bag.npy', word_bag)


def preprocess(csv_file, num_class):
    csv_divider(csv_file, num_class)
    create_word_bag()
