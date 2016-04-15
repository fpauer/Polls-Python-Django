from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from datetime import datetime

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class QuestionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(QuestionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields= ['question_text']

    def save(self, commit=True):
        question = super(QuestionForm, self).save(commit=False)
        question.user = self.request.user
        question.pub_date = datetime.now()
        if commit:
            question.save()
        return question

class ChoiceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ChoiceForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Choice
        fields= ['choice_text']

    def save(self, commit=True):
        choice = super(QuestionForm, self).save(commit=False)
        choice.user = self.request.user
        choice.pub_date = datetime.now()
        if commit:
            choice.save()
        return choice
#class ChoiceForm(Choice):
#    choice_text = forms.CharField(required=True, max_length=200)
#
#    class Meta:
#        model = Choice
#        fields = ("choice_text")