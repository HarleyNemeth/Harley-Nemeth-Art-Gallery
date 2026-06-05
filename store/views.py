from django.shortcuts import render

def index(request):
    return render(request, 'store/index.html')

def gallery(request):
    return render(request, 'store/gallery.html')

def store(request):
    return render(request, 'store/store.html')

def contact(request):
    return render(request, 'store/contact.html')

def cart(request):
    return render(request, 'store/cart.html')