from django.db import models
from django.contrib.auth.models import User



class Product(models.Model):
    CATEGORY_CHOICES = (
    ('AB', 'Amazon Books'),
    ('ONX', 'OnyxBoox'),
    ('DB', 'DigmaBooks'),
    ('PB', 'PocketBooks')
                    )
    title = models.CharField(max_length=100)
    selling_price = models.DecimalField(max_digits=7, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=15)
    composition = models.TextField(default='')
    product_image = models.ImageField(upload_to='product')
    def __str__(self):
        return self.title
    
class Customer(models.Model):
    COUNTRY_CHOICES = (('Russia', 'Russia'),
                       ('America', 'America'),
                       ('Germany', 'Germany'),
                       )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    имя = models.CharField(max_length=200)
    адрес = models.CharField(max_length=200)
    город = models.CharField(max_length=50)
    номер_телефона = models.IntegerField(default=8)
    почтовый_индекс = models.IntegerField()
    страна = models.CharField(choices=COUNTRY_CHOICES, max_length=100)
    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES = (('Принят','Принят'),
                  ('Упакован','Упакован'),
                  ('В пути','В пути'),
                  ('Доставлен','Доставлен'),
                  ('Отмена','Отмена'),
                  ('В ожидании','В ожидании'),
                  )



class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=3, max_digits=7)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='В ожидании')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default="")
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    

#models.Model - это так django понимает, что он должен сохранить его в базе данных
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    
