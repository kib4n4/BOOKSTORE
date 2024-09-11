from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Cart, CartItem, Review
from django import forms

# Extend UserCreationForm to include email field
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# Home page view displaying available books and cart count
def home(request):
    mybooks = Book.objects.all()
    cart_count = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_count = cart.items.count()
    
    context = {
        'mybooks': mybooks,
        'cart_count': cart_count
    }
    return render(request, 'home.html', context)

# Signup view with email save fix
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save the user without committing to add the email
            user.email = form.cleaned_data.get('email')  # Assign email
            user.save()  # Now save with the email
            login(request, user)  # Log in the new user
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Login view with email authentication
def login_view(request):
    if request.method == 'POST':
        email = request.POST['username']  # Use 'username' as the email input
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)  # Get user by email
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        except User.DoesNotExist:
            pass  # Optionally add error handling for non-existing email
    return render(request, 'login.html')

# Add to cart view with redirection fix
def add_to_cart(request, book_id):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, id=book_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
        if created:
            cart_item.quantity = 1  # Initialize quantity if creating a new item
        else:
            cart_item.quantity += 1  # Increment quantity if item already exists
        cart_item.save()
        return redirect(request.META.get('HTTP_REFERER', 'home'))  # Redirect back to referring page
    return redirect('login')

# View cart with total price calculation
def view_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
        total_price = sum(item.book.price * item.quantity for item in cart_items)
        return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})
    return redirect('login')

# Update cart item quantity
def update_cart_item(request, item_id):
    if request.method == "POST" and request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=item_id)
        new_quantity = int(request.POST.get('quantity', 1))
        if new_quantity > 0 and new_quantity <= cart_item.book.stock:
            cart_item.quantity = new_quantity
            cart_item.save()
        return redirect('view_cart')
    return redirect('login')

# Remove item from cart
def remove_from_cart(request, item_id):
    if request.method == "POST" and request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()
        return redirect('view_cart')
    return redirect('login')

# Clear the entire cart
def clear_cart(request):
    if request.method == "POST" and request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return redirect('view_cart')
    return redirect('login')

# Add Review with error handling for rating
def add_review(request, book_id):
    if request.method == "POST" and request.user.is_authenticated:
        book = get_object_or_404(Book, id=book_id)
        try:
            rating = int(request.POST.get('rating', 0))  # Attempt to safely convert rating to int
        except ValueError:
            rating = 0  # If invalid rating, default to 0 or handle appropriately
        comment = request.POST.get('comment', '')  # Default to empty string if no comment provided
        Review.objects.create(book=book, user=request.user, rating=rating, comment=comment)
        return redirect(request.META.get('HTTP_REFERER', 'home'))  # Redirect back to referring page
    return redirect('login')
