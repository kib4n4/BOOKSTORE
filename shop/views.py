from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Cart, CartItem, Review, Order, OrderItem
from django import forms
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q , Sum
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


# View to handle search suggestions
def search_suggestions(request):
    query = request.GET.get('query', '')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(genre__icontains=query)
        ).values('title')[:5]  # Limit to 5 suggestions
        return JsonResponse(list(books), safe=False)
    return JsonResponse([], safe=False)

# Extend UserCreationForm to include email field
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# Defining and creating the About Us page
def about(request):
    return render(request, 'about.html')

# Defining and creating the books page with filters
def books(request):
    query = request.GET.get('query', '')
    genre = request.GET.get('genre')
    author = request.GET.get('author')

    # Base queryset
    mybooks = Book.objects.all()

    # If search query is provided, filter by title, author, or genre
    if query:
        mybooks = mybooks.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(genre__icontains=query)
        )

    # If genre filter is applied
    if genre:
        mybooks = mybooks.filter(genre=genre)
    
    # If author filter is applied
    if author:
        mybooks = mybooks.filter(author=author)

    genres = Book.objects.values_list('genre', flat=True).distinct()
    authors = Book.objects.values_list('author', flat=True).distinct()

    cart_count = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_count = cart.items.count()

    context = {
        'mybooks': mybooks,
        'genres': genres,
        'authors': authors,
        'cart_count': cart_count,
        'query': query  # Pass the search query back to the template
    }

    return render(request, 'books.html', context)

# Book detail view
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = Review.objects.filter(book=book)
    context = {
        'book': book,
        'reviews': reviews,
       
    }
    return render(request, 'book_detail.html', context)

# Defining and creating the contact_submit page
def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Send an email here using the provided data
        send_mail(
            f"Message from {name}",
            message,
            email,
            ['support@bookshop.com'],  # Your support email or admin email
            fail_silently=False,
        )

        messages.success(request, 'Your message has been sent successfully.')
        return redirect('contact')
    else:
        return render(request, 'contact.html')

# Defining and creating the contact page
def contact(request):
    return render(request, 'contact.html')

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
        email = request.POST.get('email')  # Use 'email' as the input name
        password = request.POST.get('password')
        if email and password:
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    # Optionally handle authentication failure
                    return render(request, 'login.html', {'error': 'Invalid credentials'})
            except User.DoesNotExist:
                # Optionally handle user not found
                return render(request, 'login.html', {'error': 'User does not exist'})
    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('home')

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

# Checkout view
@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.book.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')

        # Create an order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            city=city,
            postal_code=postal_code,
            total_amount=total_price  # Changed to total_amount to match the Order model
        )

        # Move cart items to the order
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )
            # Reduce the stock of the book
            item.book.stock -= item.quantity
            item.book.save()

        # Clear the cart
        cart.items.all().delete()

        return redirect('order_success')

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})

# Order success page
def order_success(request):
    return render(request, 'order_success.html')

#implementing and creating admin dahsboard
def admin_dashboard(request):
    total_sales = sum(order.total_amount for order in Order.objects.all())
    total_books = Book.objects.count()
    total_orders = Order.objects.count()

    # Example sales data for the last 7 days
    sales_data = []
    sales_labels = []
    for i in range(7):
        sales_labels.append((timezone.now() - timedelta(days=i)).strftime('%Y-%m-%d'))
        sales_data.append(Order.objects.filter(order_date__date=timezone.now() - timedelta(days=i)).aggregate(Sum('total_amount'))['total_amount__sum'] or 0)

    context = {
        'total_sales': total_sales,
        'total_books': total_books,
        'total_orders': total_orders,
        'sales_data': sales_data,
        'sales_labels': sales_labels,
    }
    return render(request, 'admin/admin_dashboard.html', context)
