from django.db import models

# Create your models here.

class Topic(models.Model):
    topic_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.topic_name

class Query(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    opinion = models.TextField()


class AccessRecord(models.Model):
    name = models.ForeignKey(Query, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return str(self.date)

class Article(models.Model):
    # Author
    author = models.CharField(max_length=128)
    # Article ID
    id = models.IntegerField(unique=True, primary_key=True)
    # Link to Article
    url = models.URLField(max_length=256)
    # Article topic
    topic = models.CharField(max_length=64)
    # Article Summary
    summary = models.TextField()
    # Full text
    content = models.TextField()
    # File Path
    path = models.CharField(max_length=128)
    # Vector Embedding
    # embedding = models.CharField(max_length = 512)
