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


    tax_train_file = './cnn.bank2'

    # Read In URL File and Store in Dictionary for coupling at output
    f_url = open('url.txt', 'r')
    url = {}
    i = 0
    for l in f_url:
        url[i] = l
        i += 1

    # Read in the Corpus in the Doc2Vec specified format
    train_corpus = list(read_corpus(tax_train_file))

    #train_corpus = list(read_corpus(lee_train_file))
    #test_corpus = list(read_corpus(lee_test_file, tokens_only=True))

    print(len(train_corpus))


    # Train the Initial Model
    model = gensim.models.doc2vec.Doc2Vec(vector_size=50, min_count=2, epochs=55, seed=0)
    model.build_vocab(train_corpus)
    model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)

    model.save('model')
    seed = 0]

    #test = train_corpus[299].words

    '''
    while(1):
        # Input Function -> Parse the input text as seperate tokens

        text = input('Enter Text to Compare: ')
        parsed = text.split()
        print(parsed)

        if(parsed != []):

            model.random.seed(0)
            inferred_vector = model.infer_vector(parsed)
            sims = model.docvecs.most_similar([inferred_vector])

            print(type(inferred_vector))
            print('Inferred Vector ====> ', inferred_vector)

            print(type(sims), sims)
            print('Similar ====>', sims[0])
            #print(train_corpus[sims[0][0]].words)

        else:
            inferred_vector = model.infer_vector(['only', 'you', 'can', 'prevent', 'forest', 'fires', 'when', 'there', 'is', 'disasters',\
                                              'it', 'becomes', 'our', 'obligation', 'to', 'help', 'and', 'alleviate', 'with', 'some', 'sort', 'of', 'funding', 'or',\
                                              'other', 'ways', 'which', 'may', 'benefit', 'those', 'who', 'are', 'in', 'need'])
            sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))

    '''

    '''
    # Calculate Similarity Index above a certain threshold value
    index = 0
    sample = 0
    while(1):
        if(sims[index][1] > 0.65):
            # Output if similarity index is above threshold value
            #print('Document ({}): <{}>\n'.format(1337, ' '.join(parsed)))
            print(u'SIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % model)
            for label, index in [('MOST', 0), ('2nd', 1), ('3rd', 2)]:
                print(u'%s %s: <%s>\n' % (label, url[sims[index][0]], ' '.join(train_corpus[sims[index][0]].words)))
            break
        else:
            # Retrain the model
            print(sample, sims[index][1])
            sample += 1
            model = gensim.models.doc2vec.Doc2Vec(vector_size=50, min_count=2, epochs=55)
            model.build_vocab(train_corpus)
            model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
            sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
    '''

doc2vec('empty')
