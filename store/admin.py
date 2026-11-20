from django.contrib import admin
from .models import ArtworkImage, Category, Artwork, AboutSection, PastCommission, Order, OrderItem

admin.site.register(Category)
admin.site.register(AboutSection)


class ArtworkImageInline(admin.TabularInline):
    model = ArtworkImage
    extra = 1

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("artwork", "artwork_title", "quantity", "unit_price")
    can_delete = False


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

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "customer_email", "created_at", "total", "payment_status", "fulfillment_status")
    list_filter = ("payment_status", "fulfillment_status", "created_at")
    search_fields = ("customer_name", "customer_email", "shipping_address", "stripe_session_id")
    readonly_fields = ("stripe_session_id", "created_at", "stripe_payment_intent_id")
    ordering = ("-created_at",)
    inlines = (OrderItemInline,)


