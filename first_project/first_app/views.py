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

def writeEmbeddings(count):

    f = open("./documents/embeddings.js", "w+")
    fw = open("./documents/lin.sub.js", "w+")
    format = open("./documents/format.js", 'r+')

    for j in range(0,count):
        print('Count:', j)
        a = Article.objects.filter(id = j)
        f.write("[")
        f.write("\""+str(a[0].id)+"\",")
        f.write("\""+str(a[0].source)+"\",")

        vec = a[0].embedding
        vec = vec[1:-1]
        vec = vec.split()

        for i in range(0, len(vec)):
            if i < 299:
                f.write("\""+str(float(vec[i]))+"\",")
            else:
                f.write("\""+str(float(vec[i]))+"\"")

        f.write("],\n")

    f.seek(0)

    fw.write(format.readline())
    fw.write(format.readline())

    for line in f:
        fw.write(line)

    fw.write(format.readline())


def updateDataBase():

    info = ModelInfo.load()
    print("INFO: \n")
    print(info.article_count, info.version)

    # Populate The databases
    N = info.article_count
    l = []
    # Load New Model if Exists
    model = gensim.models.doc2vec.Doc2Vec.load(os.path.join(settings.BASE_DIR, 'documents/model'))
    bank = open('./documents/web/Articles.bank')

    while(1):
        try:

            l.append(N)
            content = bank.readline()
            content = content.split()
            inferred_vector = model.infer_vector(content)


            # Read All Files
            path = os.path.join(settings.BASE_DIR ,'./documents/web/articles/Article_'+str(N))

            f = open(path, 'r')

            id = f.readline()
            key = f.readline()
            title = f.readline()
            source = f.readline()
            source = source.rstrip('\n')
            url = f.readline()
            url = url.rstrip('\n')
            date = f.readline()

            author = f.readline()
            content = f.readline()
            summary = "#unknown"
            N += 1


            try:
                key = key.rstrip('\n')
                t = Topic.objects.filter(topic_name=key)
                num = t[0].count
                num += 1
                Topic.objects.filter(topic_name=key).update(count=num)
                print(num)
            except:
                print("Topic Exception\n", key, t.count)
                pass


            try:

                Article.objects.get_or_create(id = id, keyword = key, title = title, source = source,
                                              url = url, date = date,
                                              author=author, content = content, summary = summary,
                                              embedding = str(inferred_vector))
            except:
                pass
        except:
            print("File %s does not exist\n" % N)
            break

    info.article_count = N
    info.version += 1
    info.sublist = l
    ModelInfo.save(info)

    writeEmbeddings(N)




def index(request):

    try:
        print('In request\n')
        n = request.POST.get('remove_id',False)
        print(n, type(n))

        if n.isnumeric() :
            n = int(n)
            a = Article.objects.filter(id=n).update(display=False)
            print(a.embedding, type(a.embedding))
    except:
        pass

    articles = Article.objects.filter(display = True)
    dict = {'articles': articles}

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
    tc = 0
    subscriptions_list = ""
    topics = Topic.objects.all()



    for t in topics:
        subscriptions_list += str(t)
        subscriptions_list += ","
        tc += 1

    subscriptions_list = subscriptions_list[:-1]
    #subscriptions_list += "\'"

    if tc == 0: subscriptions_list = ""

    print("All subscriptions")
    print(subscriptions_list)

    # Used To Get Proper Path
    path = os.path.join(settings.BASE_DIR, 'documents/doc2vec.py')


    try:
        f = open('./documents/web/main.py')
    except:
        print("unable to open file")

    try:
        exe = './documents/web/main.py'
        p = subprocess.Popen(['python3', exe, subscriptions_list])
        print("Process Spawned!\n")
    except:
        print("Subprocess Not Initiated\n")



    return render(request, 'first_app/update_model.html')

def manage_subscriptions(request):

    # Get Query Set
    topic_dict = {'topic': Topic.objects.all()}

    # Subscribe to a topic
    try:
        selected_topic = request.POST['sub_topic']
        if selected_topic != '':
            Topic.objects.get_or_create(topic_name=selected_topic)[0]
            # If articles already stored locally
            a = Article.objects.filter(keyword = selected_topic)
            Topic.object.filter(topic_name = selected_topic).update(count = len(a))
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
                model = gensim.models.doc2vec.Doc2Vec.load(os.path.join(settings.BASE_DIR, 'documents/model'))
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
