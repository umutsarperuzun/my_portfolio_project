from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from .models import ContactMessage


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


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


def contact_submit(request):
    if request.method != "POST":
        return redirect('home')

    form = ContactForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Please check the form fields and try again.")
        return redirect('home')

    ContactMessage.objects.create(
        name=form.cleaned_data['name'],
        email=form.cleaned_data['email'],
        message=form.cleaned_data['message'],
    )
    messages.success(request, "Thanks! Your message has been sent.")
    return redirect('home')
