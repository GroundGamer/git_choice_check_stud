# Generated by Django 3.0.7 on 2020-06-16 19:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HeaderModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(default='', max_length=50, verbose_name='Заголовок темы')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Название формы',
                'verbose_name_plural': 'Название форм',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='QuestionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200, verbose_name='Вопрос')),
                ('question_key', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='main.HeaderModel', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Вопросы формы',
                'verbose_name_plural': 'Вопросы форм',
            },
        ),
        migrations.CreateModel(
            name='FileDateBaseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=50, verbose_name='Имя пользователя')),
                ('file_text', models.FileField(blank=True, null=True, upload_to='')),
                ('file_text_key', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.HeaderModel', verbose_name='Ключ файла')),
            ],
            options={
                'verbose_name': 'Файл с ответами',
                'verbose_name_plural': 'Файлы с ответами',
                'ordering': ['-username'],
            },
        ),
        migrations.CreateModel(
            name='AnswerModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=200)),
                ('answer_key', models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='main.QuestionModel')),
            ],
        ),
    ]
