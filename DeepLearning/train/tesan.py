# coding: utf-8
import os
import pickle
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from model_tesan import TESAN
from parameter import parse_args
from utils import load_data, get_batch, make_mask
from preprocess.preprocess import preprocess


args = parse_args()
args.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

if args.need_preprocess:
    tagged_sentences_file = 'raw_data'
    tagged_sentences_file = os.path.join(tagged_sentences_file, 'tagged_sentences.csv')
    preprocess(tagged_sentences_file)

# Load wordvecs model
w2v_model = pickle.load(open(args.WORD2VEC_DIR, 'rb'))

# load data for NTM
data_bow = np.load('dataset/word_bag.npy')
# Divide data for train and for test
data_tr = data_bow[:args.train_size]
data_te = data_bow[args.train_size:]
tensor_tr = torch.from_numpy(data_tr).float()
tensor_te = torch.from_numpy(data_te).float()

# load data for san
# text_data is a list for sentences, and label is npy.
text_data, label = load_data()
label_tr = torch.from_numpy(label[:args.train_size]).float()
label_te = torch.from_numpy(label[args.train_size:]).float()
print('Data loaded')

net_arch = args
net_arch.num_input = tensor_tr.shape[1]
net = TESAN(net_arch).cuda()
optimizer = optim.Adam(net.parameters(), args.lr, betas=(args.momentum, 0.999), weight_decay=args.wd)
criterion = nn.KLDivLoss(reduction='batchmean')

# train
for epoch in range(args.num_epoch):
    print('Epoch: ', epoch + 1)
    # Generate random indices and split it into batch
    all_indices = torch.randperm(tensor_tr.size(0)).split(args.batch_size)
    loss_epoch = 0.0
    acc = 0.0
    net.train()

    for i, batch_indices in enumerate(all_indices, 1):
        # get a batch of wordvecs
        batch_x = torch.from_numpy(get_batch(text_data, w2v_model, batch_indices, args.in_dim)).float().to(args.device)
        batch_mask = torch.from_numpy(make_mask(text_data, batch_indices, batch_x.shape[1])).float().to(args.device)

        train_input = tensor_tr[batch_indices].to(args.device)
        y = label_tr[batch_indices].to(args.device)

        recon, loss, out = net(input, batch_x, batch_mask, compute_loss=True)

        # Find max value's index
        _, pred = torch.max(out, dim=1)
        _, truth = torch.max(y, dim=1)

        num_correct = (pred == truth).sum()
        acc += num_correct.data.item()

        # sentiment loss
        sent_loss = criterion(out, y)
        total_loss = args.L * loss + sent_loss

        # optimize
        optimizer.zero_grad()
        total_loss.backward()
        optimizer.step()
        # report
        loss_epoch += total_loss.data.item()
    print('Train Loss={:.4f}, Train Acc={:.4f}'.format(loss_epoch / len(all_indices), acc / args.train_size))
    torch.save(net, '../model/model.pkl')
    # test
    all_indices = torch.arange(tensor_te.size(0)).long().split(args.batch_size)
    loss_epoch = []
    acc = []
    test_ap = []
    net.eval()
    for batch_indices in all_indices:
        # get a batch of wordvecs
        batch_x = get_batch(text_data, w2v_model, batch_indices + tensor_tr.shape[0], args.in_dim)
        with (torch.no_grad()):
            batch_x = torch.from_numpy(batch_x).float().to(args.device)
            batch_mask = torch.from_numpy(make_mask(text_data, batch_indices + tensor_tr.shape[0], batch_x.shape[1])
                                          ).float().to(args.device)

            train_input = tensor_te[batch_indices].to(args.device)
            y = label_te[batch_indices].to(args.device)

        recon, loss, out = net(input, batch_x, batch_mask, compute_loss=True)
        _, pred = torch.max(out, dim=1)
        _, truth = torch.max(y, dim=1)
        acc.extend((pred == truth).cpu().data.tolist())
        sent_loss = criterion(out, y)
        # AP
        out_exp = np.power(np.e, out.cpu().data.numpy())
        y_numpy = y.cpu().data.numpy()
        test_ap.extend([np.corrcoef(out_exp[i], y_numpy[i])[0, 1] for i in range(out_exp.shape[0])])
        # loss
        loss_epoch.append((args.L * loss + sent_loss).cpu().data.tolist())
    print('Test Loss ={:.2f},  Test Acc ={:.4f}, Test AP={:.4f}'.format(np.mean(loss_epoch), np.mean(acc),
                                                                        np.mean(test_ap)))
