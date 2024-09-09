from django.contrib import admin
from .models import Book, Cart, CartItem, Order, Review

# Admin configuration for the Book model
class BookAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('title', 'author', 'genre', 'price', 'stock', 'ratings')
    # Fields to be searchable in the admin interface
    search_fields = ('title', 'author', 'genre')
    # Filters to apply in the admin list view
    list_filter = ('genre',)

# Inline configuration for CartItem within Cart
class CartItemInline(admin.TabularInline):
    model = CartItem  # Specifies the model to use
    extra = 1  # Number of empty forms to display

# Admin configuration for the Cart model
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]  # Enables inline editing of CartItems

# Admin configuration for the Order model
class OrderAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('user', 'total_amount', 'order_date', 'status')
    # Filters to apply in the admin list view
    list_filter = ('status', 'order_date')
    # Fields to be searchable in the admin interface
    search_fields = ('user__username',)

# Admin configuration for the Review model
class ReviewAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('book', 'user', 'rating', 'comment')
    # Fields to be searchable in the admin interface
    search_fields = ('book__title', 'user__username')

# Registering the models with their respective admin configurations
admin.site.register(Book, BookAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review, ReviewAdmin)
