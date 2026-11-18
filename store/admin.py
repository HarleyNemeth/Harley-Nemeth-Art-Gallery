from django.contrib import admin
from .models import Category, Artwork, AboutSection, PastCommission

admin.site.register(Category)
admin.site.register(Artwork)
admin.site.register(AboutSection)


@admin.register(PastCommission)
class PastCommissionAdmin(admin.ModelAdmin):
    list_display = ("commission_title", "is_visible", "display_order")
    list_filter = ("is_visible",)
    search_fields = ("title", "description")
    ordering = ("display_order", "title")

    @admin.display(description="Title")
    def commission_title(self, commission):
        return commission.title or "Untitled commission"