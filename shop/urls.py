from django.urls import path
from .views import home, signup, login_view, add_to_cart, view_cart, add_review

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('add-to-cart/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('add-review/<int:book_id>/', add_review, name='add_review'),
]
