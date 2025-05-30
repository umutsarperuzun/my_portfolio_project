from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,"portfolio/home.html")

def about(request):
    return render(request,"portfolio/about.html")

def blog(request):
    return render(request,"portfolio/blog.html")

def projects(request):
    return render(request,"portfolio/projects.html")

def contact(request):
    return render(request,"portfolio/contact.html")