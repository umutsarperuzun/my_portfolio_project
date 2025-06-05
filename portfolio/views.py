from django.shortcuts import render, redirect

def home(request):
    slider_images = [
        'images/testss.png',
        'images/testss.png',
        'images/testss.png',
        'images/testss.png',
        'images/testss.png',
        'images/testss.png',
    ]
    return render(request, 'portfolio/home.html', {'slider_images': slider_images *5})

def redirect_home(request):
    return redirect('home')
