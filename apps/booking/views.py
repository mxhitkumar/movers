from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, index.html)

def contact(request):
    return render(request, index.html)

def faqs(request):
    return render(request, index.html)

def ourcompany(request):
    return render(request, index.html)

def rates(request):
    return render(request, index.html)

def blog(request):
    return render(request, index.html)

def teams(request):
    return render(request, index.html)