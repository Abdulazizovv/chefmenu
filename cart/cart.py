
from main.models import Food
from decimal import Decimal
from users.models import Kitchen

class Cart():
    def __init__(self, request) -> None:
        self.session = request.session

        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        
        self.cart = cart
    

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart.keys():
            self.cart[product_id] = {
                'product_id': product_id,
                'name': product.name,
                'price': str(product.price),
                'quantity': 1,
                'image': product.image.url,
                'kitchen_id': product.kitchen.id,
            }
        else:
            for key, value in self.cart.items():
                if key == product_id:
                    value['quantity'] += 1
                    break
        self.save()
        

    def save(self):
        self.session.modified = True
    
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def decrement(self, product):
        for key, value in self.cart.items():
            if key == str(product.id):
                value['quantity'] -= 1
                if value['quantity'] < 1:
                    self.remove(product)
                else:
                    self.save()
                break
        
    def clear(self):
        self.session['session_key'] = {}
        self.save()
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Food.objects.filter(id__in=product_ids)

        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def get_total_quantity(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price_and_quantity(self):
        return self.get_total_price(), self.get_total_quantity()
    
    def get_product(self):
        product_ids = self.cart.keys()
        products = Food.objects.filter(id__in=product_ids)
        return products
    
    def get_total_products_price(self):
        total_price = sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
        return total_price
    
    def is_empty(self):
        return len(self.cart) == 0
    
    def __str__(self):
        return str(self.cart)
    
    def __repr__(self):
        return str(self.cart)
    
    def __getitem__(self, key):
        return self.cart[key]
    
    def __setitem__(self, key, value):
        self.cart[key] = value
        self.save()

    def __delitem__(self, key):
        del self.cart[key]
        self.save()
    
    def __contains__(self, key):
        return key in self.cart
    
    def keys(self):
        return self.cart.keys()
    
    def values(self):
        return self.cart.values()
    
    def items(self):
        return self.cart.items()
    
    def clear(self):
        del self.session['session_key']
        self.save()

