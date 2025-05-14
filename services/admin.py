from django.contrib import admin
from .models import Category, Portfolio, PortfolioImage, ContactRequest, WebsiteOrderFormRequest
from users.models import Profile


class PortfolioImageInline(admin.TabularInline):
    model = PortfolioImage
    extra = 1

class PortfolioAdmin(admin.ModelAdmin):
    inlines = [PortfolioImageInline]


admin.site.register(Category)
admin.site.register(Portfolio, PortfolioAdmin)

@admin.register(ContactRequest)
class ContactRequest(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created_at', 'source')
    search_fields = ('name', 'phone', 'source')
    list_filter = ('created_at', 'source')

# admin.site.register(WebsiteOrderFormRequest)
@admin.register(WebsiteOrderFormRequest)
class WebsiteOrderFormRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'phone_number', 'price', 'created_at')
    list_filter = ('design_type', 'created_at')
    search_fields = ('title', 'description')
    fields = ('user', 'title', 'description', 'design_type', 'price')
    readonly_fields = ('phone_number', 'created_at')

    def phone_number(self, obj):
        try:
            profile = Profile.objects.get(user=obj.user)
            return profile.phone or '-'
        except Profile.DoesNotExist:
            return '-'
    phone_number.short_description = 'Phone Number'

