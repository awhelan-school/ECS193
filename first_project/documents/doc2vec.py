# Example Doc2Vec Implementation

import gensim
import os
import sys
import collections
import smart_open
import random

def read_corpus(fname, tokens_only=False):
    with smart_open.smart_open(fname, encoding="iso-8859-1") as f:
        for i, line in enumerate(f):
            if tokens_only:
                yield gensim.utils.simple_preprocess(line)
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(line), [i])

def doc2vec(inputText):

    # Set file names for train and test data
    test_data_dir = '{}'.format(os.sep).join([gensim.__path__[0], 'test', 'test_data'])
    lee_train_file = test_data_dir + os.sep + 'lee_background.cor'
    lee_test_file = test_data_dir + os.sep + 'lee.cor'


    tax_train_file = './documents/web/Articles.bank'


    # Read in the Corpus in the Doc2Vec specified format
    train_corpus = list(read_corpus(tax_train_file))

    #train_corpus = list(read_corpus(lee_train_file))
    #test_corpus = list(read_corpus(lee_test_file, tokens_only=True))

    print(len(train_corpus))


    # Train the Initial Model
    model = gensim.models.doc2vec.Doc2Vec(vector_size=50, min_count=2, epochs=1000, seed=0)
    model.build_vocab(train_corpus)

    #models.Word2Vec.intersect_word2vec_format(model,fname='./GoogleNews-vectors-negative300.bin', binary=True)
    model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)


    model.save('./documents/model_newest')
    print("Done Training.\nSaving Model!\n")

doc2vec('empty')
