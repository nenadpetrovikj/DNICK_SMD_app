from django.shortcuts import render
from django.http.response import JsonResponse

from store_basket.basket import Basket
from .models import Order, OrderItem


def add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':

        user_id = request.user.id
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        country = request.POST.get('country')
        city = request.POST.get('city')
        post_code = request.POST.get('post_code')
        order_key = request.POST.get('order_key')
        basket_total = basket.get_total_price()

        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(user_id=user_id, full_name=full_name, phone_number=phone_number, address1=address1,
                                         address2=address2, country=country, city=city, post_code=post_code, total_paid=basket_total,
                                         order_key=order_key)
            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])
        
        response = JsonResponse({'success': 'Return something'})
        return response

def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)

def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders