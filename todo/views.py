from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'todo/home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'todo/signup.html', {'form': UserCreationForm()})
    else:
        error = ''
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_todos')
            except IntegrityError:
                error = 'That username has already been taken. Please choose a new user'
        else:
            error = 'Password don`t match'
        return render(request, 'todo/signup.html', {'form': UserCreationForm(), 'error': error})


@login_required
def current_todos(request):
    todos = Todo.objects.filter(user=request.user, date_compleated__isnull=True).order_by('-created')
    return render(request, 'todo/current_todos.html', {'todos': todos})


@login_required
def completed_todos(request):
    todos = Todo.objects.filter(user=request.user, date_compleated__isnull=False).order_by('-date_compleated')
    return render(request, 'todo/completed_todos.html', {'todos': todos})


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def login_user(request):
    if request.method == 'GET':
        return render(request, 'todo/login.html', {'form': AuthenticationForm()})
    else:
        error = ''
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            error = 'Username or password don`t correct'
            return render(request, 'todo/login.html', {'form': AuthenticationForm(), 'error': error})
        else:
            login(request, user)
            return redirect('current_todos')


@login_required
def create_todo(request):
    if request.method == 'GET':
        return render(request, 'todo/create_todo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo/create_todo.html', {'form': TodoForm(), 'error': 'Bad data'})


@login_required
def detail_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/detail_todo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo/detail_todo.html', {'todo': todo, 'form': form, 'error': 'Bad data'})


@login_required
def complete_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    if request.method == 'POST':
        todo.date_compleated = timezone.now()
        todo.save()
        return redirect('current_todos')


@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current_todos')