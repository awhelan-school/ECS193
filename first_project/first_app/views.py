from django.shortcuts import render
from django.http import HttpResponse
# Background Tasks


from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic



# Import The Models
from first_app.models import Topic, Query, Article, ModelInfo

# Import Forms
from first_app.forms import QueryForm

# ROOT Folder for Documents
from django.conf import settings
import os, sys

# Doc2Vec Imports
import gensim
import collections
import smart_open
import random

def updateDataBase():

    info = ModelInfo.load()
    print("INFO: \n")
    print(info.article_count, info.version)

    # Populate The databases
    N = info.article_count

    while(1):
        try:
            # Read All Files
            path = os.path.join(settings.BASE_DIR ,'documents/web/article/Article_'+str(N))

            f = open(path, 'r')

            id = f.readline()
            key = f.readline()
            title = f.readline()
            source = f.readline()
            url = f.readline()
            url = url.rstrip('\n')
            date = f.readline()

            author = f.readline()
            summary = f.readline()
            content = f.readline()
            N += 1

            try:
                Article.objects.get_or_create(id = id, keyword = key, title = title, source = source,
                                              url = url, date = date,
                                              author=author, summary = summary, content = content)
            except:
                pass
        except:
            print("File %s does not exist\n" % N)
            break

    info.article_count = N
    info.version += 1
    ModelInfo.save(info)


def index(request):
    dict = {'insert_var': 'Value from algo computation from views.py ' + str(request)}
    return render(request, 'first_app/index.html', context=dict)


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def help(request):
    if request.method == "POST":
        help_dict = {'page_index': request}
        updateDataBase()
        return render(request, 'first_app/help.html', context=help_dict)
# Create your views here.

def home(request):
    return render(request, 'first_app/home.html')

import subprocess

def update_model(request):

    # Get All Topics
    subscriptions_list = "\'"
    topics = Topic.objects.all()

    for t in topics:
        subscriptions_list += str(t)
        subscriptions_list += ","

    subscriptions_list = subscriptions_list[:-1]
    subscriptions_list += "\'"

    print("All subscriptions")
    print(subscriptions_list)

    # Used To Get Proper Path
    path = os.path.join(settings.BASE_DIR, 'documents/doc2vec.py')


    try:
        f = open('./documents/web/main.py')
    except:
        print("unable to open file")

    try:
        print("Process Spawned!\n")
        exe = './documents/web/main.py'
        #exe = './documents/doc2vec.py'

        p = subprocess.Popen(['/Users/Whelan/anaconda3/bin/python3.6', exe, subscriptions_list])
    except:
        print("Subprocess Not Initiated\n")


    updateDataBase()

    return render(request, 'first_app/update_model.html')

def manage_subscriptions(request):

    # Get Query Set
    topic_dict = {'topic': Topic.objects.all()}

    # Subscribe to a topic
    try:
        selected_topic = request.POST['sub_topic']
        if selected_topic != '':
            Topic.objects.get_or_create(topic_name=selected_topic)[0]
    except:
        pass

    # Unsubscribe from Topic
    try:
        cancel_topic = request.POST['cancel_sub']
        cancel_topic = Topic.objects.get(topic_name = cancel_topic)
        Topic.objects.filter(topic_name=cancel_topic).delete()
    except:
        pass

    return render(request, 'first_app/manage_subscriptions.html', context=topic_dict)


def results(request):
    try:
        selected_topic = 1

    except (KeyError, Choice.DoesNotExist):
        pass

    try:
        input_text = 2
    except:
        # Redisplay the question voting form.
        return render(request, 'polls/result.html', {
            'error_message': "You didn't provide input." })


    query_dict = {'query': input_text, 'topic': selected_topic}
    return render(request, 'first_app/results.html', context=query_dict)

def make_query(request):

    # Get Query Set
    form = QueryForm()

    if request.method == "POST":
        form = QueryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)


            try:
                # Load New Model if Exists
                model = gensim.models.doc2vec.Doc2Vec.load(os.path.join(settings.BASE_DIR, 'documents/model_newest'))
                print("Using Update Model\n")
            except:
                # Load Model and Get Top 3 Similar Articles
                print("Using Base Model\n")
                model = gensim.models.doc2vec.Doc2Vec.load(os.path.join(settings.BASE_DIR ,'documents/model_base'))

            # Set Seed to add determinism
            model.random.seed(0)

            # Pre-Process Text and get embedding
            opinion = request.POST['opinion']
            opinion = opinion.split()
            inferred_vector = model.infer_vector(opinion)
            sims = model.docvecs.most_similar([inferred_vector])


            cd = {'topic': Topic.objects.get(pk=request.POST['topic']),
                  'query': request.POST['opinion'],
                  'S1': sims[0][1], 'S2': sims[1][1], 'S3': sims[2][1],
                  'S1F': Article.objects.get(pk=sims[0][0]),
                  'S2F': Article.objects.get(pk=sims[1][0]),
                  'S3F': Article.objects.get(pk=sims[2][0]), }

            # Format for S{N}
            # (Article_ID, SCORE)

            return render(request, 'first_app/results.html', context=cd)
            #return redirect('first_app:results')
        else:
            print("ERROR FORM INVALID")


    return render(request, 'first_app/make_query.html', {'form':form})
