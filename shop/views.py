from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Cart, CartItem, Review, Order, OrderItem
from django import forms
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, Sum
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Search view
def search(request):
    query = request.GET.get('query', '')
    
    # Filter books by title, author, or genre
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(genre__icontains=query)
        )

        if books.count() == 1:
            # If exactly one result, redirect to book detail page
            book = books.first()
            return redirect('book_detail', book_id=book.id)
        elif books.exists():
            # If multiple results, render the search results page
            return render(request, 'search_results.html', {'mybooks': books, 'query': query})

    # If no query or no books found, return an empty list
    return render(request, 'search_results.html', {'mybooks': [], 'query': query})

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

# About Us page
def about(request):
    mybooks =Book.objects.all()
    cart_count = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_count = cart.items.count()

    context={
        'cart_count': cart_count,
        'mybooks': mybooks,
    }

    return render(request, 'about.html',context)

# Books page with filters
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
        'cart_count': cart_count,
        'mybooks': mybooks,
        'genres': genres,
        'authors': authors,
        'cart_count': cart_count,
        'query': query
    }

    return render(request, 'books.html', context)

# Book detail view
def book_detail(request, book_id):
    mybook=Book.objects.all()
    cart_count = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_count = cart.items.count()
    book = get_object_or_404(Book, id=book_id)
    reviews = Review.objects.filter(book=book)
    context = {
        'mybook':mybook,
        'cart_count':cart_count,
        'book': book,
        'reviews': reviews,
    }
    return render(request, 'book_detail.html', context)

# Contact form submission
def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Prepare email context
        email_context = {
            'name': name,
            'email': email,
            'message': message,
            'current_year': timezone.now().year,
        }

        # Render the email template
        email_content = render_to_string('contact_email.html', email_context)

        # Send email
        send_mail(
            subject=f"Message from {name}",
            message='',
            from_email=email,
            recipient_list=['lusaboke@gmail.com'],
            html_message=email_content,  # Use the rendered HTML
            fail_silently=False,
        )

        messages.success(request, 'Your message has been sent successfully.')
        return redirect('contact')
    
    return render(request, 'contact.html')

# Contact page
def contact(request):
    return render(request, 'contact.html')

# Home page view displaying books and cart count
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

# Signup view with email inclusion
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Login view with email authentication
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'login.html', {'error': 'Invalid credentials'})
            except User.DoesNotExist:
                return render(request, 'login.html', {'error': 'User does not exist'})
    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('home')

# Add to cart view
def add_to_cart(request, book_id):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, id=book_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
        if created:
            cart_item.quantity = 1
        else:
            cart_item.quantity += 1
        cart_item.save()
        return redirect(request.META.get('HTTP_REFERER', 'home','cart'))
    return redirect('login')

def view_cart(request):
    mybooks = Book.objects.all()
    cart_count = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
        total_price = sum(item.book.price * item.quantity for item in cart_items)
        cart_count = cart.items.count()  # Update cart_count based on current cart

        context = {
            'mybooks': mybooks,
            'cart_items': cart_items,
            'total_price': total_price,
            'cart_count': cart_count,
        }
        return render(request, 'cart.html', context)
    
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

# Clear entire cart
def clear_cart(request):
    if request.method == "POST" and request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return redirect('view_cart')
    return redirect('login')

# Add review with error handling
def add_review(request, book_id):
    if request.method == "POST" and request.user.is_authenticated:
        book = get_object_or_404(Book, id=book_id)
        try:
            rating = int(request.POST.get('rating', 0))
        except ValueError:
            rating = 0
        comment = request.POST.get('comment', '')
        Review.objects.create(book=book, user=request.user, rating=rating, comment=comment)
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    return redirect('login')

# Checkout view
@login_required
def checkout(request):
    mybook = Book.objects.all()
    
    # Get the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    cart_count = cart_items.count()
    total_price = sum(item.book.price * item.quantity for item in cart_items)

    # Define the context for rendering
    context = {
        'mybook': mybook,
        'cart_count': cart_count,
        'cart_items': cart_items,
        'total_price': total_price,
    }

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
            total_amount=total_price
        )

        # Move cart items to the order and update stock
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )
            # Reduce book stock
            item.book.stock -= item.quantity
            item.book.save()

        # Clear the cart
        cart.items.all().delete()
        
        return redirect('order_success')

    return render(request, 'checkout.html', context)

# Order success page
def order_success(request):
    return render(request, 'order_success.html')

# Admin dashboard
def admin_dashboard(request):
    total_sales = sum(order.total_amount for order in Order.objects.all())
    total_books = Book.objects.count()
    total_orders = Order.objects.count()

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
