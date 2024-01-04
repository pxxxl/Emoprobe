import numpy as np
import jieba
import warnings
import os

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
    print(os.getcwd())
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
    label_path = 'train'
    label_path = os.path.join(label_path, 'dataset')
    label_path = os.path.join(label_path, 'label.npy')
    np.save(label_path, one_hot_labels)

    word_path = 'train'
    word_path = os.path.join(word_path, 'dataset')
    word_path = os.path.join(word_path, 'word.txt')
    # Divide sentences into word by jieba
    with open(word_path, 'w', encoding='utf-8') as word_file:
        for sentence in sentences:
            words = jieba.cut(sentence)
            word_file.write(' '.join(words) + '\n')
    print('Label and word files created successfully.')


def create_word_bag():
    word_path = 'train'
    word_path = os.path.join(word_path, 'dataset')
    word_path = os.path.join(word_path, 'word.txt')
    with open(word_path, 'r', encoding='utf-8') as file:
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
    vocab_path = 'model'
    vocab_path = os.path.join(vocab_path, 'vocab.npy')
    word_bag_path = 'train'
    word_bag_path = os.path.join(word_bag_path, 'dataset')
    word_bag_path = os.path.join(word_bag_path, 'word_bag.npy')
    np.save(vocab_path, vocab)
    np.save(word_bag_path, word_bag)


def preprocess(csv_file, num_class):
    csv_divider(csv_file, num_class)
    create_word_bag()
