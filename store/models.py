from typing import Any
from django.db import models


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, related_name="+"
    )  # product和collection有循环引用的问题；related_name='+'意思是不需要在Product里面创建一个collection_set，因为collection_set是一个反向关系，如果不需要反向关系，就可以用related_name='+'，这样就不会创建collection_set了，避免循环引用

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']
        verbose_name = 'Collection'
        verbose_name_plural = 'Collections'

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(
        default="-"
    )  # slug是一个短的标签，比如title是'hello world'，slug就是'hello-world'
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT
    )  # on_delete=models.PROTECT意思是如果collection被删除了，product会被保护起来，不能被删除
    promotions = models.ManyToManyField(
        Promotion
    )  # ManyToManyField意思是一个product可以有多个promotion，一个promotion可以有多个product;如果加上related_name='products'意思是在promotion里面可以通过products来访问product，比如promotion.products.all()，默认是promotion_set.all()，这是通过父级promotion查询子级的方法
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Customer(models.Model):
    MEMBERSHIP_BRONZE = "B"
    MEMBERSHIP_SILVER = "S"
    MEMBERSHIP_GOLD = "G"
    MEMBERSHIP = [
        (MEMBERSHIP_BRONZE, "Bronze"),
        (MEMBERSHIP_SILVER, "Silver"),
        (MEMBERSHIP_GOLD, "Gold"),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP, default=MEMBERSHIP_BRONZE
    )
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    class Meta:
        ordering = ['first_name', 'last_name']


class Order(models.Model):
    PAYMENT_STATUS_PENDING = "P"
    PAYMENT_STATUS_COMPLETE = "C"
    PAYMENT_STATUS_FAILED = "F"
    PAYMENT_STATUS = [
        ("P", "Pending"),
        ("C", "Complete"),
        ("F", "Failed"),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS)
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT
    )  # on_delete=models.PROTECT意思是如果customer被删除了，order会被保护起来，不能被删除


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT
    )  # on_delete=models.PROTECT意思是如果order被删除了，order_item会被保护起来，不能被删除
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT
    )  # on_delete=models.PROTECT意思是如果product被删除了，order_item会被保护起来，不能被删除
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # zip = models.CharField(max_length=255,null=False, blank=False, default="")
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, primary_key=True
    )  # customer是父级，address是子级别；models.SET_NULL意思是如果customer被删除了，address会被设置为NULL；models.SET_DEFAULT意思是如果customer被删除了，address会被设置为默认值；models.PROTECT意思是如果customer被删除了，address会被保护起来，不能被删除；models.DO_NOTHING意思是如果customer被删除了，address不会受到影响；models.CASCADE意思是如果customer被删除了，address也会被删除; primary_key=True意思不再创建id，保证customer是唯一的，一对一的关系
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE ) 一对多模型，one就是customer，是父级，一个customer可以有多个address，一个address只能有一个customer


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE
    )  # on_delete=models.CASCADE意思是如果cart被删除了，cart_item也会被删除
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
    )  # on_delete=models.CASCADE意思是如果product被删除了，cart_item也会被删除
    quantity = models.PositiveIntegerField()
