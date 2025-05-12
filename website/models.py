from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from core.settings import BASE_DIR
from storages.backends.azure_storage import AzureStorage



class User(AbstractUser):
    pass

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    # Signal to create a Customer when a User is saved
    @receiver(post_save, sender=User)
    def create_customer(sender, instance, created, **kwargs):
        if created:
            # Create a Customer instance with User's first and last name
            Customer.objects.create(user=instance, name=f'{instance.first_name} {instance.last_name}', email=instance.email)

    # Signal to save the Customer when a User is saved
    @receiver(post_save, sender=User)
    def save_customer(sender, instance, **kwargs):
        if hasattr(instance, 'customer'):
            instance.customer.save()
        
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    name = models.CharField(max_length=150, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='product/', storage=AzureStorage(), null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=150, null=True)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = float(sum([item.get_total for item in orderitems]))
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    def __str__(self):
        return str(self.id)
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    def __str__(self):
        return self.product.name + " x" + str(self.quantity)
    

class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses', null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    street = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=25)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return self.street


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length= 150)
    body = models.CharField(max_length= 500)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='question/', storage=AzureStorage(), null=True, blank=True)

    def __str__(self):
        return str(self.id)


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    body = models.CharField(max_length= 500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Challenge(models.Model):
    text = models.CharField(max_length=500)
    image = models.ImageField(upload_to='challenge/', storage=AzureStorage(), null=True)
    correct_answer = models.CharField(max_length=255)
    date = models.DateField(null=True)

    def __str__(self):
        return str(self.date)
