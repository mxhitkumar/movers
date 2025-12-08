from django.urls import path
from .views import *
from config.settings.sitemap import StaticViewSitemap, BlogSitemap  # adjust import path
from django.contrib.sitemaps.views import sitemap
from django.views.decorators.cache import cache_page

sitemaps = {
    'static': StaticViewSitemap,
}

# only add blog sitemap if BlogPost exists
try:
    from config.settings.sitemap import BlogSitemap  # same module
    sitemaps['blog'] = BlogSitemap
except Exception:
    pass

cached_sitemap = cache_page(60 * 60 * 24)(sitemap) 

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('faqs/', faqs, name='faqs'),
    path('ourcompany/', ourcompany, name='ourcompany'),
    path('rates/', rates, name='rates'),
    path('blog/', blog, name='blog'),
    path('teams/', teams, name='team'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django_sitemap'),
    path('sitemap.xml', cached_sitemap, {'sitemaps': sitemaps}, name='django_sitemap'),
]