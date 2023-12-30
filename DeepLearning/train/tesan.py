# coding: utf-8
import pickle
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
from model_tesan import TESAN
from parameter import parse_args

import os
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'




def load_data():
    # text
    text_data = []
    with open('dataset/word.txt', 'r', encoding='utf-8') as f:
        for line in f:
            text_data.append(line.strip('\n').split(' '))
    # label
    label = np.load('dataset/label.npy')

    return text_data, label


def get_batch(text_data, w2v_model, indices):
    batch_size = len(indices)
    # 一个 list 用来存储每句话的长度
    text_length = []
    for idx in indices:
        text_length.append(len(text_data[idx]))
    # 一个二维数组，存储了一个 batch 的文字信息，长为 batch_size，即 indice 的长度，宽为最长那句话的长度
    batch_x = np.zeros((batch_size, max(text_length), args.in_dim), dtype=np.float32)

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

args = parse_args()
w2v_model = pickle.load(open(args.WORD2VEC_DIR, 'rb'))

# load data for NTM
data_bow = np.load('dataset/word_bag.npy')
data_tr = data_bow[:args.train_size]
data_te = data_bow[args.train_size:]
tensor_tr = torch.from_numpy(data_tr).float()
tensor_te = torch.from_numpy(data_te).float()

# load data for san
text_data, label = load_data()
label_tr = torch.from_numpy(label[:args.train_size]).float()
label_te = torch.from_numpy(label[args.train_size:]).float()
print('Data loaded')

# test_data 是文字行的 list，label 是标签 npy

# ---------- network ----------
net_arch = args
net_arch.num_input = tensor_tr.shape[1]
net = TESAN(net_arch).cuda()
optimizer = optim.Adam(net.parameters(), args.lr, betas=(args.momentum, 0.999), weight_decay=args.wd)
criterion = nn.KLDivLoss(reduction='batchmean')

# train
for epoch in range(args.num_epoch):
    print('Epoch: ', epoch+1)

    # 生成随机索引，并将其分为制定好的 batch size
    all_indices = torch.randperm(tensor_tr.size(0)).split(args.batch_size)
    loss_epoch = 0.0
    acc = 0.0
    net.train()

    for i, batch_indices in enumerate(all_indices, 1):
        # get a batch of wordvecs
        batch_x = get_batch(text_data, w2v_model, batch_indices)
        # 格式转换，并且给 CUDA
        batch_x = Variable(torch.from_numpy(batch_x).float()).cuda()

        # 生成掩码，并作必要的格式转换
        batch_mask = make_mask(text_data, batch_indices, batch_x.shape[1])
        batch_mask = Variable(torch.from_numpy(batch_mask).float()).cuda()

        # 测试集词袋中的一批作为输入，标签集对应的一批作为输出
        input = Variable(tensor_tr[batch_indices]).cuda()
        y = Variable(label_tr[batch_indices]).cuda()

        # 由网络给出损失和输出
        recon, loss, out = net(input, batch_x, batch_mask, compute_loss=True)

        # 找出预测最大值索引和实际最大值索引
        _, pred = torch.max(out, dim=1)
        _, truth = torch.max(y, dim=1)

        # 若正确，则统计
        num_correct = (pred == truth).sum()
        acc += num_correct.data.item()

        # sentiment loss
        sent_loss = criterion(out, y)
        total_loss = args.L*loss+sent_loss

        # optimize
        optimizer.zero_grad()
        total_loss.backward()
        optimizer.step()
        # report
        loss_epoch += total_loss.data.item()
    print('Train Loss={:.4f}, Train Acc={:.4f}'.format(loss_epoch/len(all_indices), acc/args.train_size))
    torch.save(net, '../model/model.pkl')
    # test
    all_indices = torch.arange(tensor_te.size(0)).long().split(args.batch_size)
    loss_epoch = []
    acc = []
    test_ap = []
    net.eval()
    for batch_indices in all_indices:
        # get a batch of wordvecs
        batch_x = get_batch(text_data, w2v_model, batch_indices+tensor_tr.shape[0])
        # 禁用梯度计算
        with torch.no_grad():
            batch_x = Variable(torch.from_numpy(batch_x).float()).cuda()
            batch_mask = make_mask(text_data, batch_indices + tensor_tr.shape[0], batch_x.shape[1])
            batch_mask = Variable(torch.from_numpy(batch_mask).float()).cuda()

            input = Variable(tensor_te[batch_indices]).cuda()
            y = Variable(label_te[batch_indices]).cuda()

        recon, loss, out = net(input, batch_x, batch_mask, compute_loss=True)
        _, pred = torch.max(out, dim=1)
        _, truth = torch.max(y, dim=1)
        acc.extend((pred==truth).cpu().data.tolist())
        sent_loss = criterion(out, y)
        # AP
        out_exp = np.power(np.e, out.cpu().data.numpy())
        y_numpy = y.cpu().data.numpy()
        test_ap.extend([np.corrcoef(out_exp[i], y_numpy[i])[0, 1] for i in range(out_exp.shape[0])])
        # loss
        loss_epoch.append((args.L*loss+sent_loss).cpu().data.tolist())
    print('Test Loss ={:.2f},  Test Acc ={:.4f}, Test AP={:.4f}'.format(np.mean(loss_epoch),np.mean(acc),np.mean(test_ap)))