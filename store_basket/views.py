from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .basket import Basket
from store.models import Product

def basket_summary(request):
    return render(request, 'store/basket/summary.html')

def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)

        basket.add(product=product, qty=product_qty)

        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty})
        return response

def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'delete':
        product_id = int(request.POST.get('productid'))
        basket.delete(product_id=product_id)

        basketqty = basket.__len__()
        basketsubtotal = basket.get_total_price()

        response = JsonResponse({'qty': basketqty, 'subtotal': basketsubtotal})
        return response

def basket_update(request):
    basket = Basket(request)
    product_id = int(request.POST.get('productid'))
    product_qty = int(request.POST.get('productqty'))

    if request.POST.get('action') == 'post':
        basket.update(product_id=product_id, product_qty=product_qty)

    elif request.POST.get('action') == 'delete':
        basket.update(product_id=product_id, product_qty=product_qty, delete=True)
    
    basketqty = basket.__len__()
    basketproductprice = basket.get_product_with_quantity_price(product_id=product_id)
    baskettotal = basket.get_total_price()

    response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal, 
                             'productqty': basket.get_qty(product_id=product_id),
                             'productprice': basketproductprice})
    return response