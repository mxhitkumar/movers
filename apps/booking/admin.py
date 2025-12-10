from django.contrib import admin
from django.utils.html import format_html
from .models import SEOSettings, ContactSubmission, MovingRequest


admin.site.site_header = "Gati Expert"  # Changes the main header text
admin.site.site_title = "Expert Gati Movers and Packers"    # Changes the HTML <title> tag and the text in the browser tab
admin.site.index_title = "Welcome to Your Expert Gati Portal" # Changes the text on the admin index page


@admin.register(SEOSettings)
class SEOSettingsAdmin(admin.ModelAdmin):
    list_display = [
        'page_name',
        'meta_title_preview',
        'has_og_image',
        'has_twitter_image',
        'has_schema',
        'robots',
        'preview_button'
    ]
    
    list_filter = ['robots', 'og_type', 'twitter_card']
    
    search_fields = ['page_name', 'meta_title', 'meta_description', 'meta_keywords']
    
    fieldsets = (
        ('Page Identification', {
            'fields': ('page_name',),
            'description': 'Unique identifier for this page'
        }),
        ('Basic SEO Meta Tags', {
            'fields': (
                'meta_title',
                'meta_description',
                'meta_keywords',
                'canonical_url',
                'robots'
            ),
            'description': 'Primary SEO settings. Meta title: 50-60 chars, Description: 150-160 chars'
        }),
        ('Open Graph (Facebook)', {
            'classes': ('collapse',),
            'fields': (
                'og_title',
                'og_description',
                'og_image',
                'og_type'
            ),
            'description': 'Settings for Facebook and other social platforms using Open Graph'
        }),
        ('Twitter Card', {
            'classes': ('collapse',),
            'fields': (
                'twitter_title',
                'twitter_description',
                'twitter_image',
                'twitter_card'
            ),
            'description': 'Settings specific to Twitter sharing'
        }),
        ('Structured Data (Schema.org)', {
            'classes': ('collapse',),
            'fields': ('schema_json',),
            'description': 'JSON-LD structured data for search engines. Leave blank to use defaults.'
        }),
        ('Additional Scripts', {
            'classes': ('collapse',),
            'fields': ('extra_header',),
            'description': 'Analytics, tracking pixels, or other header scripts'
        }),
    )
    
    readonly_fields = []
    
    def meta_title_preview(self, obj):
        """Show meta title with character count"""
        title = obj.get_meta_title()
        length = len(title)
        
        if length > 60:
            color = 'red'
            status = '⚠️'
        elif length < 50:
            color = 'orange'
            status = '⚠️'
        else:
            color = 'green'
            status = '✓'
        
        return format_html(
            '<span style="color: {};">{} {} chars</span><br/><small>{}</small>',
            color,
            status,
            length,
            title[:60] + '...' if length > 60 else title
        )
    meta_title_preview.short_description = 'Meta Title (50-60 chars)'
    
    def has_og_image(self, obj):
        """Check if OG image exists"""
        if obj.og_image:
            return format_html(
                '<span style="color: green;">✓ Yes</span>'
            )
        return format_html(
            '<span style="color: orange;">✗ No</span>'
        )
    has_og_image.short_description = 'OG Image'
    
    def has_twitter_image(self, obj):
        """Check if Twitter image exists"""
        if obj.twitter_image:
            return format_html(
                '<span style="color: green;">✓ Yes</span>'
            )
        return format_html(
            '<span style="color: orange;">✗ No</span>'
        )
    has_twitter_image.short_description = 'Twitter Image'
    
    def has_schema(self, obj):
        """Check if custom schema exists"""
        if obj.schema_json:
            return format_html(
                '<span style="color: green;">✓ Custom</span>'
            )
        return format_html(
            '<span style="color: blue;">✓ Default</span>'
        )
    has_schema.short_description = 'Schema'
    
    def preview_button(self, obj):
        """Add a preview button"""
        return format_html(
            '<a class="button" href="#" onclick="alert(\'Preview functionality - connect to your view\'); return false;">Preview</a>'
        )
    preview_button.short_description = 'Actions'
    
    class Media:
        css = {
            'all': ('admin/css/seo_admin_custom.css',)  # Optional: create this for custom styling
        }
        js = ('admin/js/seo_admin_custom.js',)  # Optional: create this for custom JS
    
    def save_model(self, request, obj, form, change):
        """Add custom save logic if needed"""
        super().save_model(request, obj, form, change)
        
        # You can add logic here, like:
        # - Clear cache when SEO settings change
        # - Send notifications
        # - Log changes
        
    def get_readonly_fields(self, request, obj=None):
        """Make certain fields readonly for non-superusers"""
        readonly = list(self.readonly_fields)
        
        if not request.user.is_superuser:
            readonly.extend(['robots', 'schema_json', 'extra_header'])
        
        return readonly


# Optional: Inline admin for related models if you have any
# Example if you want to manage SEO for multiple pages in one place

class SEOSettingsInline(admin.TabularInline):
    model = SEOSettings
    extra = 0
    fields = ['page_name', 'meta_title', 'meta_description']
    show_change_link = True


# Optional: Custom admin action to duplicate SEO settings
def duplicate_seo_settings(modeladmin, request, queryset):
    """Admin action to duplicate SEO settings"""
    for seo in queryset:
        seo.pk = None
        seo.page_name = f"{seo.page_name} (Copy)"
        seo.save()
    
    modeladmin.message_user(
        request,
        f"{queryset.count()} SEO setting(s) duplicated successfully."
    )

duplicate_seo_settings.short_description = "Duplicate selected SEO settings"

# Add the action to the admin
SEOSettingsAdmin.actions = [duplicate_seo_settings]

from django.contrib import admin
from .models import ContactSubmission

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "service", "created_at")
    readonly_fields = ("created_at", "ip_address")
    search_fields = ("name", "email", "phone", "message")

@admin.register(MovingRequest)
class MovingRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "location_from", "location_to", "date", "created_at")
    readonly_fields = ("created_at",)