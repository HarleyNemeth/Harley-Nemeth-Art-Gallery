from django.contrib import admin
from .models import ArtworkImage, Category, Artwork, AboutSection, PastCommission

admin.site.register(Category)
admin.site.register(AboutSection)


class ArtworkImageInline(admin.TabularInline):
    model = ArtworkImage
    extra = 1


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "available",
        "stock",
        "display_order",
    )
    list_editable = ("display_order",)
    list_filter = ("category", "available")
    search_fields = ("title",)
    ordering = ("display_order", "-created_at", "pk")
    inlines = (ArtworkImageInline,)


@admin.register(PastCommission)
class PastCommissionAdmin(admin.ModelAdmin):
    list_display = ("commission_title", "is_visible", "display_order")
    list_filter = ("is_visible",)
    search_fields = ("title", "description")
    ordering = ("display_order", "title")

    @admin.display(description="Title")
    def commission_title(self, commission):
        return commission.title or "Untitled commission"