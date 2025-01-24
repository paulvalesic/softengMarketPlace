from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .forms import UserRegistrationForm, ItemForm, OrderReviewForm
from .models import User, Item, Order, Review
from user_messages.models import Message
from django.contrib.auth.decorators import login_required
from django.db import transaction, models
from django.contrib import messages
from django.db.models import Q, Count

# --------------------------
# Autentifikacija i dashboard
# --------------------------
@login_required
def buyer_dashboard(request):
    if not request.user.is_buyer:
        return redirect('seller_dashboard')

    chat_partners = User.objects.filter(
        Q(received_messages__sender=request.user) | 
        Q(sent_messages__receiver=request.user)
    ).distinct().annotate(
        last_message_time=models.Max(
            models.Case(
                models.When(received_messages__sender=request.user, 
                        then='received_messages__created_at'),
                models.When(sent_messages__receiver=request.user, 
                        then='sent_messages__created_at'),
                output_field=models.DateTimeField()
            )
        ),
        unread_count=models.Count(
            models.Case(
                models.When(received_messages__is_read=False,
                        received_messages__sender=request.user,
                        then=1),
                default=models.Value(0),
                output_field=models.IntegerField()
            )
        )
    ).order_by('-last_message_time')

    partners_with_messages = []
    for partner in chat_partners:
        last_message = Message.objects.filter(
            Q(sender=request.user, receiver=partner) |
            Q(sender=partner, receiver=request.user)
        ).order_by('-created_at').first()
        
        partners_with_messages.append({
            'partner': partner,
            'unread': partner.unread_count,
            'last_message': last_message.content if last_message else None,
            'timestamp': last_message.created_at if last_message else None
        })
    
    orders = request.user.orders.all().order_by('-created_at')
    
    return render(request, 'accounts/buyer_dashboard.html', {
        'orders': orders,
        'chat_partners': partners_with_messages
    })

@login_required
def seller_dashboard(request):
    if not request.user.is_seller:
        return redirect('buyer_dashboard')
    
    chat_partners = User.objects.filter(
        Q(received_messages__sender=request.user) | 
        Q(sent_messages__receiver=request.user)
    ).distinct().annotate(
        last_message_time=models.Max(
            models.Case(
                models.When(received_messages__sender=request.user, 
                        then='received_messages__created_at'),
                models.When(sent_messages__receiver=request.user, 
                        then='sent_messages__created_at'),
                output_field=models.DateTimeField()
            )
        ),
        unread_count=models.Count(
            models.Case(
                models.When(received_messages__is_read=False,
                        received_messages__sender=request.user,
                        then=1),
                default=models.Value(0),
                output_field=models.IntegerField()
            )
        )
    ).order_by('-last_message_time')

    partners_with_messages = []
    for partner in chat_partners:
        last_message = Message.objects.filter(
            Q(sender=request.user, receiver=partner) |
            Q(sender=partner, receiver=request.user)
        ).order_by('-created_at').first()
        
        partners_with_messages.append({
            'partner': partner,
            'unread': partner.unread_count,
            'last_message': last_message.content if last_message else None,
            'timestamp': last_message.created_at if last_message else None,
            'item': last_message.item if last_message else None
        })

    items = request.user.items.all()
    orders = Order.objects.filter(item__seller=request.user).order_by('-created_at')
    
    return render(request, 'accounts/seller_dashboard.html', {
        'items': items,
        'orders': orders,
        'chat_partners': partners_with_messages
    })

# --------------------------
# Narudžbe i recenzije
# --------------------------
@login_required
def submit_review(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    
    if order.status != 'Confirmed':
        return redirect('buyer_dashboard')

    existing_review = Review.objects.filter(order=order).first()

    if request.method == 'POST':
        form = OrderReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user 
            review.reviewed_user = order.item.seller
            review.order = order
            review.save()
            return redirect('buyer_dashboard')
    else:
        form = OrderReviewForm(instance=existing_review)

    return render(request, 'accounts/submit_review.html', {
        'form': form,
        'order': order
    })

@login_required
def confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.user == order.item.seller:
        order.status = 'Confirmed'
        order.save()
        return redirect('seller_dashboard')
    
    return redirect('home')

# --------------------------
# Registracija i login
# --------------------------
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.get(email=email)
        if user.check_password(password):
            login(request, user)
            return redirect('home')
    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

# --------------------------
# Profil i artikli
# --------------------------
@login_required
def user_dashboard(request):
    user = request.user
    
    if user.is_seller:
        items = user.items.all()
        orders = Order.objects.filter(item__seller=user).order_by('-created_at')
        return render(request, 'accounts/seller_dashboard.html', {
            'user': user,
            'items': items,
            'orders': orders,
        })
    
    elif user.is_buyer:
        orders = user.orders.all()
        chat_partners = User.objects.filter(
            Q(received_messages__sender=user) | 
            Q(sent_messages__receiver=user)
        ).distinct().annotate(
            unread_messages=Count('received_messages', filter=Q(received_messages__is_read=False))
        )
        
        return render(request, 'accounts/buyer_dashboard.html', {
            'user': user,
            'orders': orders,
            'chat_partners': [(u, u.unread_messages) for u in chat_partners]
        })
    
    else:
        return redirect('home')

def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    items = user.items.all()
    orders = user.orders.all()
    reviews = user.reviews_received.all()
    return render(request, 'accounts/profile.html', {
        'user': user,
        'items': items,
        'orders': orders,
        'reviews': reviews,
    })

@login_required
def post_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
            return redirect('seller_dashboard')
    else:
        form = ItemForm()
    return render(request, 'accounts/post_item.html', {'form': form})

# --------------------------
# Transakcije
# --------------------------
@login_required
def place_order(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    context = {'item': item}
    
    if request.method == 'POST':
        if item.quantity < 1:
            messages.error(request, "This item is out of stock!")
            return redirect('home')
        
        user_balance = request.user.token_balance
        item_price = item.price
        
        if user_balance >= item_price:
            try:
                with transaction.atomic():
                    request.user.token_balance -= item_price
                    request.user.save()
                    
                    seller = item.seller
                    seller.token_balance += item_price
                    seller.save()
                    
                    order = Order.objects.create(
                        buyer=request.user,
                        item=item,
                        status='Pending'
                    )
                    
                    item.quantity -= 1
                    item.save()
                    
                    messages.success(request, "Order placed successfully!")
                    return redirect('buyer_dashboard')
                    
            except Exception as e:
                messages.error(request, f"Error processing order: {str(e)}")
        else:
            messages.error(request, "Insufficient token balance to complete this purchase!")
        
        return redirect('item_detail', item_id=item.id)
    
    return render(request, 'accounts/place_order.html', context)

def review_user(request, user_id):
    reviewed_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewed_user = reviewed_user
            review.save()
            return redirect('profile', user_id=user_id)
    else:
        form = ReviewForm()
    return render(request, 'accounts/review_user.html', {'form': form, 'reviewed_user': reviewed_user})