# DeepLearning

EmoProbe allow you to build your own custom dataset and train on it.

## Preprocess

You can generate your own dataset and define emotion as you like in preprocess.

### Custom dataset

EmoProbe allow you to build your own custom dataset and train on it. 

If you have ready-made dataset, make sure it's organize as csv, and it should looks like:

```
0, I'm happy!
1, Oh, it's sucks!
4, That's disgusting.
1, I can't stand it.
```

The number represent some kind of emotion, and it can define by yourself. To get best accuracy, the numbers of sentences should more that 1000.

If you don't have ready-made dataset, you make want to create one by yourself. We provide a maunal tagger for you to tag sentences. need a txt file that content enough sentences, and you can

### Data process

TESAN can't use csv file as dataset directly, it need some data preprocess.

You can run `DeepLearning/train/preprocess/preprocess.py` to preprocess the data. After that, you can start training by TESAN

## Train

To start training, use the following command:

```
python tesan.py [--train_size] [--test_size] [--num_class]
```


- ``train_size``: 
- ``test_size``: 
- ``num_class``: 