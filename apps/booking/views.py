from django.shortcuts import render
from booking.models import SEOSettings

# Create your views here.


def home(request):
    page_name = "Home"
    seo = SEOSettings.objects.get(page_name="Home")
    return render(request, "pages/home.html", {"seo": seo})


def contact(request):
    page_name = "Contact"
    return render(request, "pages/contact.html")


def faqs(request):
    page_name = "FAQs"
    return render(request, "pages/faqs.html")


def ourcompany(request):
    page_name = "OurCompany"
    return render(request, "pages/our-company.html")


def rates(request):
    page_name = "Rates"
    return render(request, "pages/rates.html")


def blog(request):
    page_name = "Blog"
    return render(request, "pages/blog.html")


def teams(request):
    page_name = "Teams"
    return render(request, "pages/team.html")
