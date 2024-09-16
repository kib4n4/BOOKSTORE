from django.contrib import admin
from .models import Book, Cart, CartItem, Order, Review

# Admin configuration for the Book model
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'price', 'stock', 'ratings', 'image')  # Added image to display
    search_fields = ('title', 'author', 'genre')
    list_filter = ('genre',)

# Inline configuration for CartItem within Cart
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

# Admin configuration for the Cart model
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]

# Admin configuration for the Order model
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_amount', 'order_date', 'status')
    list_filter = ('status', 'order_date')
    search_fields = ('user__username',)

# Admin configuration for the Review model
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'comment')
    search_fields = ('book__title', 'user__username')

# Registering the models with their respective admin configurations
admin.site.register(Book, BookAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review, ReviewAdmin)
