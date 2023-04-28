from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login

from .forms import RegisterForm
from api.views import home


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'registration/register.html', {'form': form})
    elif request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have signed up successfully.')
            login(request, user)
            return redirect(home)
        else:
            return render(request, 'registration/register.html', {'form': form})