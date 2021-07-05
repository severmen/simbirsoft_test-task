from django.db import models, router


# Create your models here.
class Question(models.Model):
    uuid = models.IntegerField()
    text = models.CharField(max_length=400, verbose_name="Текст самого вопроса")

class Choice(models.Model):
    text = models.CharField(max_length=150, verbose_name="Текст варианта ответа")
    is_correct = models.BooleanField(verbose_name="правильность ответа")
    Question = models.ForeignKey(Question, on_delete=models.CASCADE)


    def __str__(self):
        return self.text



