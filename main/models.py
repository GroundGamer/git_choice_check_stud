from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class HeaderModel(models.Model):
    header = models.CharField(max_length=50, verbose_name='Заголовок темы', default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Название формы'
        verbose_name_plural = 'Название форм'
        ordering = ['-created_at']

    def __str__(self):
        return '%s - %s' % (self.header, self.author)


class QuestionModel(models.Model):
    question = models.CharField(max_length=200, verbose_name='Вопрос')
    question_key = models.ForeignKey(HeaderModel, on_delete=models.CASCADE, verbose_name='Пользователь', default='')

    class Meta:
        verbose_name = 'Вопросы формы'
        verbose_name_plural = 'Вопросы форм'

    def __str__(self):
        return '%s - %s' % (self.question, self.question_key)


class AnswerModel(models.Model):
    answer = models.CharField(max_length=200)
    answer_key = models.ForeignKey(QuestionModel, on_delete=models.PROTECT, default='')


class FileDateBaseModel(models.Model):
    username = models.CharField(max_length=50, verbose_name='Имя пользователя', default='')
    file_text = models.FileField(null=True, blank=True)
    file_text_key = models.ForeignKey(HeaderModel, on_delete=models.SET_NULL,
                                      null=True, blank=True, verbose_name='Ключ файла', default='')

    class Meta:
        verbose_name = 'Файл с ответами'
        verbose_name_plural = 'Файлы с ответами'
        ordering = ['-username']

    def __str__(self):
        return '%s' % self.file_text
