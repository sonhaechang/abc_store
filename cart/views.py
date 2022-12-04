from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from cart.models import Cart
from cart.services import SessionCart


# Create your views here.
def cart_list(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).select_related('user')
    else:
        cart = SessionCart(request)

    return render(request, 'cart/container/cart_list.html', {
        'cart_list': cart,
    })