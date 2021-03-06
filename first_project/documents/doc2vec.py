# Example Doc2Vec Implementation

import gensim
from gensim import *
import os
import sys
from collections import *
import smart_open
import random
import matplotlib.pyplot as plt
import math
import requests

def plot_distribution(corpus):

    doc_count = len(corpus)
    doc_length =[]

    for index in range(0, doc_count):
        doc_length.append(len(corpus[index].words))

    num_bins = 200
    n, bins, patches = plt.hist(doc_length, bins='auto', facecolor='blue',
                                alpha=None, histtype='barstacked', edgecolor='black')

    plt.xlabel('Document Text Length')
    plt.ylabel('Document Count')
    plt.title('Document Text Length Distribution')
    plt.show()

def test_conv(model, corpus, color, type):

    #corpus = corpus[:150]

    sample_taken = 0

    doc_count = len(corpus)

    doc_index = 0
    sample_size = 10
    # Sample Text to match
    avg_text_length = 0

    # Total Words in All articles
    total_words = 0

    # Track SIMILAR
    sim_dict = defaultdict(lambda:0)
    sample_dict = OrderedDict()
    score_dict = OrderedDict()

    while(doc_index < doc_count):

        total_words += len(corpus[doc_index].words)

        while(sample_size < len(corpus[doc_index].words)):

            sample_taken += 1.0
            try:
                sample_dict[sample_size] += 1
            except:
                sample_dict[sample_size] = 1

            # Test Similarity with variable sample text size
            sample_text = corpus[doc_index].words
            model.random.seed(0)
            inferred_vector = model.infer_vector(sample_text[0:sample_size])
            sims = model.docvecs.most_similar([inferred_vector], topn=1)

            # If prediction is correct, break to next article
            if(sims[0][0] == doc_index):

                score = sims[0][1]

                # Add Score Value at N Sample text Size
                try:
                    score_dict[sample_size] += score
                except:
                    score_dict[sample_size] = score


                avg_text_length += sample_size/sample_taken
                # Add Similar Score if correct
                sim_dict[sample_size] += sims[0][1] / doc_count
                sample_size += 10
            # Otherwise increase sample text size
            else:
                sample_size += 10


        # Next Document
        sample_taken = 0
        doc_index += 1
        sample_size = 10

    avg_doc_length = math.floor(total_words/doc_count)

    print(avg_text_length/doc_count)
    print(avg_doc_length)

    # For Graph
    # sample size list - X axis
    samples = []
    # Similarity Score - Y Axis
    sim_score = []

    x = 10

    while(x < avg_doc_length):
        samples.append(x)
        sim_score.append(score_dict[x]/sample_dict[x])
        x += 10

    # plotting the points
    plt.plot(samples, sim_score, color, label=type)

    # naming the x axis
    plt.xlabel('Sample Text Size')
    # naming the y axis
    plt.ylabel('Similarity Score')

    # giving a title to my graph
    plt.title('Similarity Score Based on Text Sample')
    plt.legend()

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

    #pre_model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)
    #print(pre_model.most_similar('dog'))

    #try:
    #    model = gensim.models.doc2vec.Doc2Vec.load('model')
    #    print("Loaded Existing Model.\n")
    #except:
    #    print("No Previous Model Saved!\nTraining New Model.\n")
        # Train the Initial Model


    model = gensim.models.doc2vec.Doc2Vec(vector_size=300, min_count=7, epochs=20, dm=1, window=5, workers=4)
    model.build_vocab(train_corpus)
    models.Word2Vec.intersect_word2vec_format(model, fname='./documents/GoogleNews-vectors-negative300.bin', binary=True)  # C binary format
    model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)


    # Convergence Plots/Tests

    # test_conv(model, train_corpus, 'r', 'unsupervised')

    #model2 = gensim.models.doc2vec.Doc2Vec(vector_size=300, min_count=7, epochs=20, dm=1, window=5, workers=4)
    #model2.build_vocab(train_corpus)
    #models.Word2Vec.intersect_word2vec_format(model2, fname='./GoogleNews-vectors-negative300.bin', binary=True)  # C binary format
    #model2.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
    #test_conv(model2, train_corpus, 'g', 'supervised')

    #plt.show()
    #plt.legend()
    #plot_distribution(corpus=train_corpus)
    print("Saving Model.\n")
    model.save('./documents/model')
    requests.post('http://127.0.0.1:8000/help/')


doc2vec('empty')
