from django import forms
from django.forms import inlineformset_factory

from .models import *


class QuestionForm(forms.ModelForm):
    class Meta:
        model = HeaderModel
        fields = ('header',)


class AnswerForm(forms.ModelForm):
    class Meta:
        model = AnswerModel
        fields = '__all__'


QuestionFormSet = inlineformset_factory(HeaderModel, QuestionModel, fields='__all__')
