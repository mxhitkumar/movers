from django.db import models
from django.urls import reverse

class SEOSettings(models.Model):
    page_name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Name to identify the page (e.g. Home, About, Services)",
    )

    # Basic SEO
    meta_title = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        help_text="Recommended: 50-60 characters"
    )
    meta_description = models.TextField(
        blank=True, 
        null=True,
        help_text="Recommended: 150-160 characters"
    )
    canonical_url = models.URLField(blank=True, null=True)
    
    # Keywords for better SEO
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Comma-separated keywords"
    )

    # Open Graph
    og_title = models.CharField(max_length=255, blank=True, null=True)
    og_description = models.TextField(blank=True, null=True)
    og_image = models.ImageField(upload_to="seo/", blank=True, null=True)
    og_type = models.CharField(
        max_length=50,
        default="website",
        blank=True,
        null=True
    )

    # Twitter
    twitter_title = models.CharField(max_length=255, blank=True, null=True)
    twitter_description = models.TextField(blank=True, null=True)
    twitter_image = models.ImageField(upload_to="seo/", blank=True, null=True)
    twitter_card = models.CharField(
        max_length=50,
        default="summary_large_image",
        blank=True,
        null=True
    )

    # Schema JSON
    schema_json = models.TextField(
        blank=True, null=True, help_text="Paste full JSON-LD schema here"
    )

    # Extra header scripts like tracking codes
    extra_header = models.TextField(
        blank=True, null=True, help_text="Add extra scripts (analytics, pixels…)"
    )
    
    # SEO Settings
    robots = models.CharField(
        max_length=100,
        default="index, follow",
        blank=True,
        null=True,
        help_text="e.g., index, follow or noindex, nofollow"
    )

    def __str__(self):
        return self.page_name
    
    def get_meta_title(self):
        """Return meta title or generate default"""
        if self.meta_title:
            return self.meta_title
        return f"{self.page_name} - Expert Gati Packers and Movers | Pune & Mumbai"
    
    def get_meta_description(self):
        """Return meta description or generate default"""
        if self.meta_description:
            return self.meta_description
        return "Expert Gati Packers and Movers - Professional moving services in Pune, Mumbai & All India. Safe, reliable & affordable home & office relocation services."
    
    def get_og_title(self):
        """Return OG title or fall back to meta title"""
        return self.og_title or self.get_meta_title()
    
    def get_og_description(self):
        """Return OG description or fall back to meta description"""
        return self.og_description or self.get_meta_description()
    
    def get_twitter_title(self):
        """Return Twitter title or fall back to meta title"""
        return self.twitter_title or self.get_meta_title()
    
    def get_twitter_description(self):
        """Return Twitter description or fall back to meta description"""
        return self.twitter_description or self.get_meta_description()
    
    def get_default_schema(self):
        """Generate default LocalBusiness schema if none provided"""
        if self.schema_json:
            return self.schema_json
        
        default_schema = {
            "@context": "https://schema.org",
            "@type": "MovingCompany",
            "name": "Expert Gati Packers and Movers",
            "description": "Professional packers and movers service in Pune, Mumbai and across India",
            "url": "https://www.expertgatipackers.com",
            "telephone": "+91-XXXXXXXXXX",
            "priceRange": "$$",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Your Street Address",
                "addressLocality": "Pune",
                "addressRegion": "Maharashtra",
                "postalCode": "411001",
                "addressCountry": "IN"
            },
            "areaServed": [
                {
                    "@type": "City",
                    "name": "Pune"
                },
                {
                    "@type": "City",
                    "name": "Mumbai"
                },
                {
                    "@type": "Country",
                    "name": "India"
                }
            ],
            "serviceType": [
                "Home Relocation",
                "Office Relocation",
                "Packing Services",
                "Loading and Unloading",
                "Storage Services"
            ]
        }
        
        import json
        return json.dumps(default_schema)
    
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    published = models.BooleanField(default=False)   # optional
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})  # ensure this url exists

    def __str__(self):
        return self.title
    
class ContactSubmission(models.Model):
    SERVICE_CHOICES = [
        ("", "-- Select One --"),
        ("Office Moving", "Office Moving"),
        ("Home Moving", "Home Moving"),
        ("International Moving", "International Moving"),
        ("Pet Moving", "Pet Moving"),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, blank=True)
    message = models.TextField()
    botcheck = models.CharField(max_length=255, blank=True, help_text="Honeypot field")
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.email} ({self.created_at:%Y-%m-%d %H:%M})"
    