import csv
import os
import datetime

from django.shortcuts import render, redirect
from django.utils.http import urlquote

from .models import HeaderModel, QuestionModel, FileDateBaseModel
from .forms import QuestionForm, QuestionFormSet, AnswerForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest


def user_show(request):
    return render(request, 'main/index.html')


def redirect_user(request):
    if request.method == 'GET':
        user_choice = request.GET.get('user_choice')
        if user_choice == 'Студент':
            return redirect('main:stud')
        elif user_choice == 'Преподователь':
            return redirect('main:teach')
        else:
            return redirect('main:index')


def show_page_question(request):
    questions = HeaderModel.objects.filter(author=request.user.pk)
    context = {'questions': questions}

    return render(request, 'main/page_question.html', context)


def detail_check(request, pk):
    header_check = get_object_or_404(HeaderModel, pk=pk)
    question_check = QuestionModel.objects.filter(question_key=pk)
    form = AnswerForm()

    context = {'header_check': header_check, 'question_check': question_check, 'form': form}

    if request.method == 'POST':
        answer_dict = {}
        name = request.POST.get('FIO')
        answer_dict['name'] = name
        query_dict = str(request.POST)
        l_query = query_dict.rfind("'answer'")
        r_query = query_dict.rfind("'submit'")
        final_query = query_dict[l_query + 11:r_query - 3:].replace(", ", ",").replace("'", "")
        list_query = final_query.split(',')
        answer_dict['answer'] = list_query
        now_day = datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
        title_file = str(header_check) + ' - ' + str(name) + ' - ' + now_day + '.csv'

        with open("media/" + title_file, 'w', newline="") as file_handler:
            columns = ["name", "answer"]
            writer = csv.DictWriter(file_handler, fieldnames=columns)
            writer.writeheader()
            writer.writerow(answer_dict)

        file_mode_save = FileDateBaseModel(username=name, file_text=title_file, file_text_key_id=header_check.id)
        file_mode_save.save()
        return redirect('main:stud')

    return render(request, 'main/detail_page.html', context)


def static_detail_page(request, file_text_id, pk):
    list_question = []
    question = HeaderModel.objects.filter(author=request.user.id)
    questions_check = QuestionModel.objects.filter(question_key_id=file_text_id)
    file_text = FileDateBaseModel.objects.filter(pk=pk)
    list_str_question = str(questions_check).replace('<QuestionModel:', '').replace('<QuerySet [ ', '')\
        .replace('>]>', '')\
        .replace('>', '').split(', ')
    for i in list_str_question:
        l_question = i.find(' - ')
        list_question.append(i[:l_question:])

    file_name = str(FileDateBaseModel.objects.get(pk=pk).file_text)
    path_download = 'media/' + file_name

    if os.path.exists(path_download):
        with open(path_download) as fl:
            reader = csv.DictReader(fl)
            for row in reader:
                str_answer = row['answer'].replace('[', '').replace(']', '').replace("'", "")
                list_answer = str_answer.split(', ')

    dict_answer = dict(zip(list_question, list_answer))

    context = {'questions': question,
               'questions_check': questions_check,
               'files_text': file_text,
               'dict_answer': dict_answer}

    return render(request, 'main/static_detail_page.html', context)


def static_page_answer(request):
    questions = HeaderModel.objects.filter(author=request.user.id)
    questions_check = QuestionModel.objects.filter(question_key__author=request.user.id)
    files_text = FileDateBaseModel.objects.filter(file_text_key__author=request.user.id)

    context = {'questions': questions, 'questions_check': questions_check, 'files_text': files_text}

    return render(request, 'main/static_page_answer.html', context)


class QuestionCreate(CreateView):
    model = HeaderModel
    template_name = 'main/page_add_question.html'
    form_class = QuestionForm
    success_url = reverse_lazy('main:show_page_question')

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        question_form = QuestionFormSet()
        return self.render_to_response(self.get_context_data(form=form, question_form=question_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.instance.author_id = request.user.id
        question_form = QuestionFormSet(self.request.POST)
        if form.is_valid() and question_form.is_valid():
            return self.form_valid(form, question_form)
        else:
            return self.render_to_response(self.get_context_data(form=form, question_form=question_form))

    def form_valid(self, form, question_form):
        form.instance.user = self.request.user
        self.object = form.save()
        question_form.instance = self.object
        question_form.save()

        return HttpResponseRedirect(self.get_success_url())


class QuestionUpdate(UpdateView):
    model = HeaderModel
    template_name = 'main/update_question.html'
    form_class = QuestionForm
    success_url = reverse_lazy('main:show_page_question')

    def get(self, request, *args, **kwargs):
        question = HeaderModel.objects.get(id=kwargs['pk'])
        self.object = None
        form = QuestionForm(instance=question)
        question_form = QuestionFormSet(instance=question)
        return self.render_to_response(self.get_context_data(form=form, question_form=question_form))

    def post(self, request, *args, **kwargs):
        question = HeaderModel.objects.get(id=kwargs['pk'])
        self.object = None
        form = QuestionForm(self.request.POST, instance=question)
        form.instance.author_id = request.user.id
        question_form = QuestionFormSet(self.request.POST, instance=question)
        if form.is_valid():
            return self.form_valid(form, question_form)
        else:
            return self.render_to_response(self.get_context_data(form=form, question_form=question_form))

    def form_valid(self, form, question_form):
        form.instance.user = self.request.user
        self.object = form.save()
        question_form.instance = self.object
        question_form.save()

        return HttpResponseRedirect(self.get_success_url())


def delete_question(request, pk):
    if request.user.is_authenticated:
        question = HeaderModel.objects.get(id=pk)
        question.delete()
        return redirect('main:show_page_question')
    else:
        return HttpResponseBadRequest


def stud_question(request):
    questions = HeaderModel.objects.all()
    question_id = request.user.id
    context = {'questions': questions, 'question_filter': question_id}
    return render(request, 'main/stud_question.html', context)


class UserLoginView(LoginView):
    template_name = 'main/auth_teach.html'


class UserLogoutView(LogoutView, LoginRequiredMixin):
    template_name = 'main/index.html'


def about(request):
    return render(request, 'main/about.html')
