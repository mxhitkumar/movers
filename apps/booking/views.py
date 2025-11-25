from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "pages/index.html")

def contact(request):
    return render(request, "pages/contact.html")

def faqs(request):
    return render(request, "pages/faqs.html")

def ourcompany(request):
    return render(request, "pages/our-company.html")

def rates(request):
    return render(request, "pages/rates.html")

def blog(request):
    return render(request, "pages/blog.html")

def teams(request):
    return render(request, "pages/team.html")