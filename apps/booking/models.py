from django.db import models

# Create your models here.
from django.db import models


class SEOSettings(models.Model):
    page_name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Name to identify the page (e.g. Home, About, Services)",
    )

    # Basic SEO
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    canonical_url = models.URLField(blank=True, null=True)

    # Open Graph
    og_title = models.CharField(max_length=255, blank=True, null=True)
    og_description = models.TextField(blank=True, null=True)
    og_image = models.ImageField(upload_to="seo/", blank=True, null=True)

    # Twitter
    twitter_title = models.CharField(max_length=255, blank=True, null=True)
    twitter_description = models.TextField(blank=True, null=True)
    twitter_image = models.ImageField(upload_to="seo/", blank=True, null=True)

    # Schema JSON
    schema_json = models.TextField(
        blank=True, null=True, help_text="Paste full JSON-LD schema here"
    )

    # Extra header scripts like tracking codes
    extra_header = models.TextField(
        blank=True, null=True, help_text="Add extra scripts (analytics, pixels…)"
    )

    def __str__(self):
        return self.page_name
