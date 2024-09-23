from django.urls import path
from .views import (
    search_suggestions, 
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
    book_detail  # Import book_detail here
)

urlpatterns = [
    path('', home, name='home'),
    path('search/', books, name='search'),
    path('search-suggestions/', search_suggestions, name='search_suggestions'),  # Add this for AJAX suggestions
    path('book/<int:book_id>/', book_detail, name='book_detail'),  # Fixed the URL pattern
    path('books/', books, name='books'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('contact/submit/', contact_submit, name='contact_submit'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add-to-cart/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/update/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', clear_cart, name='clear_cart'),
    path('add-review/<int:book_id>/', add_review, name='add_review'),
    path('checkout/', checkout, name='checkout'),
    path('order-success/', order_success, name='order_success'),
]
