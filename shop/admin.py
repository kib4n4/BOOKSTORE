from django.contrib import admin
from .models import Book, Cart, CartItem, Order, Review

# Admin configuration for the Book model
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'price', 'stock', 'ratings', 'image')  # Display essential fields
    search_fields = ('title', 'author', 'genre')
    list_filter = ('genre',)
    ordering = ('title',)  # Default ordering by title

# Inline configuration for CartItem within Cart
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    min_num = 1  # Ensure at least one item is present

# Admin configuration for the Cart model
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ('user',)  # Display user associated with the cart
    search_fields = ('user__username',)

# Admin configuration for the Order model
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_amount', 'order_date', 'status')
    list_filter = ('status', 'order_date')
    search_fields = ('user__username',)
    ordering = ('-order_date',)  # Default ordering by order date

# Admin configuration for the Review model
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'comment')
    search_fields = ('book__title', 'user__username')
    list_filter = ('rating',)  # Filter reviews by rating

# Custom Admin Site Configuration
class CustomAdminSite(admin.AdminSite):
    site_header = "Books & More Books Admin"
    site_title = "Admin Dashboard"
    index_title = "Welcome to the Admin Dashboard"

# Registering the models with their respective admin configurations
admin.site = CustomAdminSite(name='custom_admin')
admin.site.register(Book, BookAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review, ReviewAdmin)
