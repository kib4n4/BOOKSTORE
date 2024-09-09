from django.contrib.auth.models import User  # Use the default User model
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField()
    ratings = models.FloatField(default=0.0)

    def __str__(self):
        return (f"Title: {self.title}, Author: {self.author}, Genre: {self.genre}, "
                f"Description: {self.description[:50]}..., Price: ${self.price:.2f}, "
                f"Stock: {self.stock}, Ratings: {self.ratings}")

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, through='CartItem')

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.book.title} in {self.cart}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, related_name='orders')
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    shipping_address = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} - {self.status}"

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Review of {self.book.title} by {self.user.username}"
