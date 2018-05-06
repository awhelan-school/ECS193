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
    # Article ID
    id = models.IntegerField(unique=True, primary_key=True)
    # Keyword
    keyword = models.CharField(max_length=128)
    # Title
    title = models.CharField(max_length=128)
    # Source
    source = models.CharField(max_length=128)
    # Link to Article
    url = models.URLField(max_length=256)
    # Date of Article
    date = models.DateField()
    # Author
    author = models.CharField(max_length=128)
    # Article Summary
    summary = models.TextField()
    # Full text
    content = models.TextField()
    # Vector Embedding
    # embedding = models.CharField(max_length = 512)

# id
# Keyword
# Title
# Source
# URL
# Date
# Author
# Summary
# Content

class ModelInfo(models.Model):
    article_count = models.IntegerField(unique=True)
    version = models.IntegerField()


    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(ModelInfo, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()