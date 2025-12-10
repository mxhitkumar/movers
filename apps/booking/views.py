from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .forms import ContactForm, MovingRequestForm
from .models import SEOSettings, ContactSubmission
from django.contrib import messages
from django.core.mail import send_mail  # for email notifications (optional)


def get_or_create_seo(page_name, defaults):
    """Helper function to get or create SEO settings"""
    try:
        seo = SEOSettings.objects.get(page_name=page_name)
    except ObjectDoesNotExist:
        seo = SEOSettings.objects.create(page_name=page_name, **defaults)
    return seo


def home(request):
    """Home page view"""
    seo = get_or_create_seo(
        page_name="Home",
        defaults={
            'meta_title': "Expert Gati Packers and Movers Pune | Best Moving Company Mumbai",
            'meta_description': "Expert Gati Packers and Movers - #1 Trusted Packers and Movers in Pune & Mumbai. Professional home & office shifting services across India. Get FREE quotes! ✓Safe ✓Reliable ✓Affordable",
            'meta_keywords': "packers and movers pune, movers pune, packers movers mumbai, home shifting pune, office relocation pune, best packers movers pune, gati packers pune",
            'canonical_url': request.build_absolute_uri(),
            'og_title': "Expert Gati Packers and Movers - Pune & Mumbai's #1 Moving Company",
            'og_description': "Professional packing & moving services in Pune, Mumbai & across India. 10+ years experience, 5000+ happy customers. Get instant free quote!",
            'twitter_title': "Expert Gati Packers and Movers - Pune & Mumbai",
            'twitter_description': "Trusted packers and movers in Pune & Mumbai. Safe, affordable & professional relocation services across India."
        }
    )
    
    if request.method == "POST":
        form = MovingRequestForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.ip_address = request.META.get("REMOTE_ADDR")
            instance.save()

            # Optional: send email notification (configure EMAIL settings)
            # send_mail(
            #     subject=f"New contact from {instance.name}",
            #     message=instance.message,
            #     from_email=instance.email,
            #     recipient_list=["you@yourdomain.com"],
            # )

            messages.success(request, "Thanks! Your message has been sent. We'll contact you shortly.")
            return redirect("home")  # reload page (seo will be reloaded)
        else:
            # Form invalid — show errors and SEO together
            messages.error(request, "Please fix the errors below.")
    else:
        form = MovingRequestForm()

    # Render page with both seo and form (works for GET and invalid POST)
    return render(request, "pages/home.html", {"seo": seo, "form": form})


def contact(request):
    """Contact page view — handles form POST and always provides SEO data."""
    # Ensure SEO is available for both GET and POST renderings
    seo = get_or_create_seo(
        page_name="Contact",
        defaults={
            'meta_title': "Contact Us - Expert Gati Packers and Movers Pune | Get Free Quote",
            'meta_description': "Contact Expert Gati Packers and Movers for relocation services in Pune & Mumbai. Call us for FREE quotes. Available 24/7. Email, phone & visit our office for best moving rates.",
            'meta_keywords': "contact packers movers pune, packers movers phone number pune, movers contact mumbai, free quote packers movers, relocation inquiry pune",
            'canonical_url': request.build_absolute_uri(),
            'og_title': "Contact Expert Gati Packers and Movers - Get Free Moving Quote",
            'og_description': "Get in touch with Pune & Mumbai's trusted moving company. Free quotes, 24/7 support, instant response. Call now for relocation assistance!",
            'twitter_title': "Contact Expert Gati Packers - Free Moving Quote",
            'twitter_description': "Need movers in Pune or Mumbai? Contact us for instant free quotes and professional moving services."
        }
    )

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.ip_address = request.META.get("REMOTE_ADDR")
            instance.save()

            # Optional: send email notification (configure EMAIL settings)
            # send_mail(
            #     subject=f"New contact from {instance.name}",
            #     message=instance.message,
            #     from_email=instance.email,
            #     recipient_list=["you@yourdomain.com"],
            # )

            messages.success(request, "Thanks! Your message has been sent. We'll contact you shortly.")
            return redirect("contact")  # reload page (seo will be reloaded)
        else:
            # Form invalid — show errors and SEO together
            messages.error(request, "Please fix the errors below.")
    else:
        form = ContactForm()

    # Render page with both seo and form (works for GET and invalid POST)
    return render(request, "pages/contact.html", {"seo": seo, "form": form})


def faqs(request):
    """FAQs page view"""
    seo = get_or_create_seo(
        page_name="FAQs",
        defaults={
            'meta_title': "FAQs - Packers and Movers Questions Answered | Expert Gati Pune",
            'meta_description': "Frequently asked questions about packers and movers services in Pune & Mumbai. Get answers on pricing, packing, insurance, moving process, and more. Expert Gati answers all your queries.",
            'meta_keywords': "packers movers faqs pune, moving questions answers, relocation faq mumbai, packing services questions, moving cost queries pune",
            'canonical_url': request.build_absolute_uri(),
            'og_title': "Moving FAQs - All Your Packing & Moving Questions Answered",
            'og_description': "Common questions about hiring packers and movers in Pune & Mumbai. Learn about costs, timelines, insurance, and the moving process.",
            'twitter_title': "Packers & Movers FAQs - Expert Gati Pune",
            'twitter_description': "Got questions about moving? Find answers to common queries about packers and movers services in Pune & Mumbai."
        }
    )
    return render(request, "pages/faqs.html", {"seo": seo})


def ourcompany(request):
    """Our Company page view"""
    seo = get_or_create_seo(
        page_name="OurCompany",
        defaults={
            'meta_title': "About Expert Gati Packers and Movers | 10+ Years Moving Experience",
            'meta_description': "Learn about Expert Gati Packers and Movers - Pune & Mumbai's trusted moving company since 2013. 10+ years experience, 5000+ happy customers, professional team. Know our story & values.",
            'meta_keywords': "about expert gati packers, moving company pune history, best movers mumbai, trusted packers movers pune, professional relocation company",
            'canonical_url': request.build_absolute_uri(),
            'og_title': "About Expert Gati Packers - Leading Moving Company in Pune & Mumbai",
            'og_description': "Discover why Expert Gati is Pune & Mumbai's most trusted moving company. 10+ years of excellence, certified professionals, 5000+ successful relocations.",
            'twitter_title': "About Expert Gati Packers and Movers",
            'twitter_description': "10+ years of moving excellence in Pune & Mumbai. Meet the team behind India's trusted relocation services."
        }
    )
    return render(request, "pages/our-company.html", {"seo": seo})


def rates(request):
    """Rates page view"""
    seo = get_or_create_seo(
        page_name="Rates",
        defaults={
            'meta_title': "Packers and Movers Rates in Pune & Mumbai | Affordable Moving Charges",
            'meta_description': "Check transparent packers and movers rates in Pune & Mumbai. Affordable home & office shifting charges. No hidden costs. Get detailed pricing for local & interstate moves. Compare and save!",
            'meta_keywords': "packers movers rates pune, moving charges mumbai, relocation cost pune, shifting charges pune mumbai, affordable movers prices, moving cost calculator",
            'canonical_url': request.build_absolute_uri(),
            'og_title': "Affordable Packers & Movers Rates - Pune & Mumbai Pricing",
            'og_description': "Transparent pricing for all moving services. Check detailed rates for home shifting, office relocation & more in Pune & Mumbai. Best prices guaranteed!",
            'twitter_title': "Moving Rates Pune & Mumbai - Expert Gati",
            'twitter_description': "Affordable and transparent packers and movers rates in Pune & Mumbai. No hidden charges. Get your free quote today!"
        }
    )
    return render(request, "pages/rates.html", {"seo": seo})


def blog(request):
    """Blog page view"""
    seo = get_or_create_seo(
        page_name="Blog",
        defaults={
            'meta_title': "Moving Tips & Guides Blog | Expert Gati Packers and Movers Pune",
            'meta_description': "Read expert moving tips, packing guides, and relocation advice. Learn how to plan your move in Pune & Mumbai. Home shifting tips, office relocation guides & more on our blog.",
            'meta_keywords': "moving tips blog, packing guides pune, relocation advice mumbai, home shifting tips, office moving blog, packers movers articles",
            'canonical_url': request.build_absolute_uri(),
            'og_title': "Moving & Packing Tips Blog - Expert Advice from Gati Movers",
            'og_description': "Expert advice on moving, packing, and relocation. Read our blog for tips to make your move in Pune & Mumbai smooth and stress-free.",
            'twitter_title': "Moving Tips Blog - Expert Gati Packers",
            'twitter_description': "Get expert moving tips, packing hacks, and relocation guides. Your complete resource for stress-free moving in Pune & Mumbai."
        }
    )
    return render(request, "pages/blog.html", {"seo": seo})


def teams(request):
    """Teams page view"""
    seo = get_or_create_seo(
        page_name="Teams",
        defaults={
            'meta_title': "Our Professional Moving Team | Expert Gati Packers and Movers",
            'meta_description': "Meet our experienced and professional moving team. Trained packers, skilled drivers, and courteous staff in Pune & Mumbai. Certified professionals committed to safe relocations.",
            'meta_keywords': "professional movers team pune, expert packers staff, trained moving crew mumbai, certified relocation team, experienced movers pune",
            'canonical_url': request.build_absolute_uri(),
            'og_title': "Meet Our Professional Moving Team - Expert Gati Pune & Mumbai",
            'og_description': "Our certified moving professionals are ready to handle your relocation. Experienced, trained, and committed to excellence in Pune & Mumbai.",
            'twitter_title': "Our Moving Team - Expert Gati Packers",
            'twitter_description': "Meet the professional team behind Pune & Mumbai's most trusted moving company. Experienced, certified, and customer-focused."
        }
    )
    return render(request, "pages/team.html", {"seo": seo})
