from django.shortcuts import render, get_object_or_404, redirect
from .models import Artwork, AboutSection
from django.http import JsonResponse

def index(request):
    featured = Artwork.objects.filter(featured=True).first()
    about = AboutSection.objects.first()
    return render(request, 'store/index.html', {'featured': featured, 'about': about})

def store(request):
    artworks = Artwork.objects.all()
    return render(request, 'store/store.html', {'artworks': artworks})

from django.core.mail import send_mail
from .forms import ContactForm

def contact(request):
    sent = False

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            send_mail(
                subject=f'New enquiry from {name}',
                message=f'From: {name} ({email})\n\n{message}',
                from_email=None,
                recipient_list=['dracohcn@gmail.com'],
            )
            sent = True
            form = ContactForm()
    else:
        form = ContactForm()

    return render(request, 'store/contact.html', {'form': form, 'sent': sent})

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
    artwork = get_object_or_404(Artwork, id=artwork_id)
    cart = request.session.get('cart', {})
    key = str(artwork_id)

    current_qty = cart.get(key, 0)

    if current_qty >= artwork.stock:
        return JsonResponse({
            'success': False,
            'message': 'Sorry, this item is out of stock.'
        })

    if key in cart:
        cart[key] += 1
    else:
        cart[key] = 1

    request.session['cart'] = cart
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