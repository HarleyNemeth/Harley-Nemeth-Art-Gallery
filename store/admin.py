from django.contrib import admin
from .models import Category, Artwork, AboutSection, CommissionOffering

admin.site.register(Category)
admin.site.register(Artwork)
admin.site.register(AboutSection)


@admin.register(CommissionOffering)
class CommissionOfferingAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("title", "description")
    ordering = ("display_order", "title")