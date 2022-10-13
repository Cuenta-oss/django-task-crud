from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class modelTask(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'modelTask'
        verbose_name_plural = 'modelTasks'

    def __str__(self):
        return self.title
