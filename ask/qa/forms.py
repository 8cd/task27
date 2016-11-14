from django import forms
from qa.models import Question, Answer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
"""
class AskForm(forms.Form):
	title = forms.CharField(max_length=50)
	text = forms.CharField(widget=forms.Textarea)

	def clean(self):
		return self.cleaned_data

	def save(self):
		self.cleaned_data['author'] = self._user
		return Question.objects.create(**self.cleaned_data)
"""
"""
class AnswerForm(forms.Form):
	text = forms.CharField(widget=forms.Textarea)
	question = forms.IntegerField(widget=forms.HiddenInput)

	def clean(self):
		return self.cleaned_data

	def save(self):
		self.cleaned_data['author'] = self._user
		self.cleaned_data['question'] = Question.objects.get(pk=self._question)
		return Answer.objects.create(**self.cleaned_data)

"""
class AskForm(forms.Form):
	title = forms.CharField(max_length=50)
	text = forms.CharField(widget=forms.Textarea)

	def clean_title(self):
		title = self.cleaned_data.get('title')
		if len(title) < 3:
			raise forms.ValidationError('Title is a short. Min length 3')
		return title

	def clean_text(self):
		text = self.cleaned_data.get('text')
		if len(text) < 3:
			raise forms.ValidationError('Text is a short. Min length 3')
		return text

	def save(self):
		question = Question(**self.cleaned_data)
		question.author = self._user
		question.save()
		return question




class AnswerForm(forms.Form):
	text = forms.CharField(widget=forms.Textarea)
	question = forms.IntegerField(widget=forms.HiddenInput)

	def clean_text(self):
		answer = self.cleaned_data.get('text')
		if not answer:
			raise forms.ValidationError('Answer text can\'t be blank.')
		return answer

	def clean_question(self):
		id = self.cleaned_data.get('question')
		try:
			question = Question.objects.get(pk=id)
		except Question.DoesNotExist:
			raise forms.ValidationError('Question not founded.')
		return question
    
	def save(self):
		answer = Answer(**self.cleaned_data)
		answer.author = self._user
		answer.save()
		return answer


class SignupForm(forms.Form):
	username = forms.CharField(max_length=20)
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput)

	def save(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		email = self.cleaned_data.get('email')
		user = User.objects.create_user(username, email, password)
		user.save()
		return user

class LoginForm(forms.Form):
	username = forms.CharField(max_length=200)
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		self.user = authenticate(username=username, password=password)
		if self.user is not None:
			if not self.user.is_active:
				raise forms.ValidationError('Disabled account')
		else:
			raise forms.ValidationError('Invalid login')

	def get_user(self):
		return self.user