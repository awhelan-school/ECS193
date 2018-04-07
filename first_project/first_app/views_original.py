from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

# Import The Models
from first_app.models import Topic

def index(request):
    dict = {'insert_var': 'Value from algo computation from views.py ' + str(request)}
    return render(request, 'first_app/index.html', context=dict)

def help(request):
    help_dict = {'page_index': request}
    return render(request, 'first_app/help.html', context=help_dict)
# Create your views here.

def home(request):
    return render(request, 'first_app/home.html')

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

def make_query(request):

    # Get Query Set
    topic_dict = {'topic': Topic.objects.all()}

    return render(request, 'first_app/make_query.html', context=topic_dict)

def results(request):

    try:
        selected_topic = request.POST['sel_topic']

    except (KeyError, Choice.DoesNotExist):
        pass

    try:
        input_text = request.POST['input_text']
    except:
        # Redisplay the question voting form.
        return render(request, 'polls/result.html', {
            'error_message': "You didn't provide input." })

    print("HERE")
    query_dict = {'query': input_text, 'topic': selected_topic}
    return render(request, 'first_app/results.html', context=query_dict)
