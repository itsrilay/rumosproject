from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Customer, Product, Address, OrderItem, Order, Category, Question, Answer, Challenge

admin.site.register(User, UserAdmin)
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Challenge)