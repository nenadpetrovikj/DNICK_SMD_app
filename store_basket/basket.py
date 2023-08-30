from decimal import Decimal
from django.conf import settings
from store.models import Product

class Basket():

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)

        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
            
        self.basket = basket

    def add(self, product, qty):
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product.price), 'qty': int(qty)}

        self.save()
    
    def delete(self, product_id):
        product_id = str(product_id)

        if product_id in self.basket:
            del self.basket[product_id]
            
        self.save()

    def update(self, product_id, product_qty, delete=False):
        product_id = str(product_id)

        if product_id in self.basket:
            if delete:
                if self.basket[product_id]['qty'] == 1:
                    self.delete(product_id=product_id)
                else:
                    self.basket[product_id]['qty'] -= product_qty
            else:
                self.basket[product_id]['qty'] += product_qty

        self.save()

    def save(self):
        self.session.modified = True
    
    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product
        
        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        return sum(item['qty'] for item in self.basket.values())
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
    
    def get_product_with_quantity_price(self, product_id):
        product_id = str(product_id)

        if product_id in self.basket:
            return self.basket[product_id]['qty'] * Decimal(self.basket[product_id]['price'])
        return 0

    def get_qty(self, product_id):
        product_id = str(product_id)

        if product_id in self.basket:
            return self.basket[product_id]['qty']
        return 0
    
    def clear(self):
        # Remove basket from session
        del self.session[settings.BASKET_SESSION_ID]
        self.save()