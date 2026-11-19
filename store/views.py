from django.shortcuts import render, get_object_or_404, redirect
from .models import Artwork, AboutSection, Category, PastCommission
from django.http import JsonResponse
from django.db import transaction
from django.conf import settings

def index(request):
    featured = Artwork.objects.filter(featured=True).first()
    about = AboutSection.objects.first()
    return render(
        request,
        "store/index.html",
        {
            "featured": featured,
            "about": about,
        },
    )

def store(request):
    artworks = Artwork.objects.select_related('category').prefetch_related(
        'additional_images'
    )
    artwork_sections = [
        {
            'id': 'available-artworks',
            'heading': 'Available Artwork',
            'artworks': artworks.filter(
                available=True,
                stock__gt=0,
            ).order_by('display_order', '-created_at', 'pk'),
        },
        {
            'id': 'sold-out-artworks',
            'heading': 'Sold Out',
            'artworks': artworks.filter(
                available=True,
                stock=0,
            ).order_by('display_order', '-created_at', 'pk'),
        },
        {
            'id': 'not-offered-artworks',
            'heading': 'Not Currently Offered',
            'artworks': artworks.filter(
                available=False,
            ).order_by('display_order', '-created_at', 'pk'),
        },
    ]
    categories = Category.objects.filter(
        artworks__isnull=False
    ).distinct().order_by('name', 'pk')
    return render(
        request,
        'store/store.html',
        {
            'artworks': artworks,
            'artwork_sections': artwork_sections,
            'categories': categories,
        },
    )

from django.core.mail import send_mail
from .forms import ContactForm

def contact(request):
    sent = False

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            inquiry_label = dict(ContactForm.INQUIRY_CHOICES)[data["inquiry_type"]]
            message_parts = [
                f"Enquiry type: {inquiry_label}",
                f"From: {data['name']} ({data['email']})",
            ]
            for label, field in (
                ("Preferred size or format", "project_size"),
                ("Approximate budget", "budget"),
                ("Ideal timeframe", "timeframe"),
            ):
                if data[field]:
                    message_parts.append(f"{label}: {data[field]}")
            message_parts.extend(("", data["message"]))

            send_mail(
                subject=f"{inquiry_label} from {data['name']}",
                message="\n".join(message_parts),
                from_email=None,
                recipient_list=[settings.CONTACT_EMAIL],
            )
            sent = True
            form = ContactForm()
    else:
        initial = {}
        inquiry_type = request.GET.get("enquiry_type")
        allowed_types = {choice[0] for choice in ContactForm.INQUIRY_CHOICES}
        if inquiry_type in allowed_types:
            initial["inquiry_type"] = inquiry_type

        form = ContactForm(initial=initial)

    return render(
        request,
        "store/contact.html",
        {
            "form": form,
            "sent": sent,
            "past_commissions": PastCommission.objects.filter(is_visible=True),
        },
    )

def cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for artwork_id, quantity in cart.items():
        try:
            artwork = Artwork.objects.get(id=int(artwork_id))
            subtotal = artwork.price * quantity
            total += subtotal
            items.append({
                'artwork': artwork,
                'quantity': quantity,
                'subtotal': subtotal,
            })
        except Artwork.DoesNotExist:
            pass

    return render(request, 'store/cart.html', {'items': items, 'total': total})

def add_to_cart(request, artwork_id):
    with transaction.atomic():
        artwork = get_object_or_404(Artwork, id=artwork_id)
        if not artwork.available or artwork.stock <= 0:
            return JsonResponse({
                'success': False,
                'message': 'This artwork is not available for purchase'
            })

        cart = request.session.get('cart', {})
        key = str(artwork_id)
        current_qty = cart.get(key, 0)

        if current_qty >= artwork.stock:
            return JsonResponse({
                'success': False,
                'message': 'No more stock available'
            })

        cart[key] = current_qty + 1
        request.session['cart'] = cart
        request.session.modified = True

        return JsonResponse({
            'success': True,
            'cart_count': sum(cart.values())
        })
def remove_from_cart(request, artwork_id):
    cart = request.session.get('cart', {})
    key = str(artwork_id)
    if key in cart:
        del cart[key]
    request.session['cart'] = cart
    return redirect('cart')