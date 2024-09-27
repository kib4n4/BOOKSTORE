from django.urls import path
from . import views
from .views import (
    search_suggestions, 
    admin_dashboard,
    contact_submit, 
    home, 
    books, 
    signup, 
    login_view, 
    logout_view, 
    add_to_cart, 
    view_cart, 
    update_cart_item, 
    remove_from_cart, 
    clear_cart, 
    add_review, 
    checkout, 
    order_success, 
    about, 
    contact,
    book_detail,
)

urlpatterns = [
    # Home Page
    path('', home, name='home'),

    # Search and Suggestions
    path('search/', books, name='search'),  # Handles the search page
    path('search-suggestions/', search_suggestions, name='search_suggestions'),  # Real-time search suggestions

    # Book Details and Listing
    path('book/<int:book_id>/', book_detail, name='book_detail'),  # Individual book detail page
    path('books/', books, name='books'),  # Book listing page

    # Static Pages
    path('about/', about, name='about'),  # About us page
    path('contact/', contact, name='contact'),  # Contact page
    path('contact/submit/', contact_submit, name='contact_submit'),  # Contact form submission

    # User Authentication
    path('signup/', signup, name='signup'),  # User registration
    path('login/', login_view, name='login'),  # User login
    path('logout/', logout_view, name='logout'),  # User logout

    # Cart Management
    path('add-to-cart/<int:book_id>/', add_to_cart, name='add_to_cart'),  # Add book to cart
    path('cart/', view_cart, name='view_cart'),  # View cart
    path('cart/update/<int:item_id>/', update_cart_item, name='update_cart_item'),  # Update cart item
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),  # Remove item from cart
    path('cart/clear/', clear_cart, name='clear_cart'),  # Clear entire cart

    # Reviews and Orders
    path('add-review/<int:book_id>/', add_review, name='add_review'),  # Add a book review
    path('checkout/', checkout, name='checkout'),  # Checkout process
    path('order-success/', order_success, name='order_success'),  # Order success page

    # Admin Dashboard
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),  # Admin dashboard
]
