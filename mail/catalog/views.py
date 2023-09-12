from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect,  get_object_or_404
from .models import Letter, Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, LetterForm, ProfileEditForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

def index(request):
    return render(request, "index.html")

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Создан аккаунт {username}')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'register.html', {'form':form})

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('main')

@login_required
def main(request):
    num_users = User.objects.all().count()
    num_letters = Letter.objects.all().count()
    num_profiles=Profile.objects.all().count()
    letters = Letter.objects.filter(to_user=request.user)
    return render(request, 'main.html', context = {'num_users':num_users,
												   'num_letters':num_letters,
												   'num_profiles':num_profiles,
												   'letters':letters})

@login_required
def logout(request):
	return render(request, 'logout.html')


class LetterListView(generic.ListView):
	model = Letter
	paginate_by = 1


class LetterDetailView(generic.DetailView):
	model = Letter
	author = User.username

class LetterCreateView(LoginRequiredMixin, CreateView):
	model = Letter
	fields=['to_user', 'theme', 'content']
	#author = User.username
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

@login_required
def input(request):
	letters = Letter.objects.filter(to_user=request.user)
	num_input = letters.count()
	return render(request, 'input.html', context = {'num_input':num_input,
												   'letters':letters})

@login_required
def output(request):
	letters = Letter.objects.filter(author=request.user)
	num_output = letters.count()
	return render(request, 'output.html', context = {'num_output':num_output,
												   'letters':letters})

@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileEditForm(request.POST,
								   request.FILES,
								   instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Ваш профиль успешно обновлен.')
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileEditForm(instance=request.user.profile)
	context = {
		'u_form': u_form,
		'p_form': p_form
	}
	return render(request, 'profile.html', context)

import xlwt
#excel

def export_users(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="users.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Users')

	# Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Имя пользователя', 'Пароль']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	# Sheet body, remaining rows
	font_style = xlwt.XFStyle()

	rows = User.objects.all().values_list('username', 'password')
	for row in rows:
		row_num += 1
		for col_num in range(len(row)):
			ws.write(row_num, col_num, row[col_num], font_style)

	wb.save(response)
	return response

import datetime
def export_letters(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="letters.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Letters')

	# Sheet header, first row
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Отправитель', 'Получатель', 'Тема', 'Содержание', 'Дата отправки']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	# Sheet body, remaining rows
	font_style = xlwt.XFStyle()

	rows = Letter.objects.all().values_list('author', 'to_user', 'theme', 'content', 'date_sended')
	for row in rows:
		row_num += 1
		for col_num in range(len(row)):
			if isinstance(row[col_num], datetime.datetime):
				date_time = row[col_num].strftime('%Y-%m-%d %H:%M:%S')
				ws.write(row_num, col_num, date_time, font_style)
			else:
				ws.write(row_num, col_num, row[col_num], font_style)

	wb.save(response)
	return response