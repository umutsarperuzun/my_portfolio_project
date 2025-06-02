from django.shortcuts import render, redirect

def home(request):
    return render(request, 'portfolio/home.html')

def redirect_home(request):
    return redirect('home')
