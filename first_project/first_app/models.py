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
