from django.shortcuts import render, redirect, get_object_or_404
from .forms import MessageForm
from .models import Message
from accounts.models import User, Item
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from .models import Message


@login_required
def send_message(request, receiver_id, item_id=None):
    receiver = get_object_or_404(User, id=receiver_id)
    item = get_object_or_404(Item, id=item_id) if item_id else None

    messages = Message.objects.filter(
        Q(sender=request.user, receiver=receiver) |
        Q(sender=receiver, receiver=request.user)
    ).order_by('created_at')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.item = item
            message.save()
            return redirect('send_message', receiver_id=receiver.id)
    else:
        form = MessageForm(initial={'content': ''})

    if receiver != request.user:
        messages.filter(is_read=False).update(is_read=True)

    return render(request, 'user_messages/chat.html', {
        'form': form,
        'receiver': receiver,   
        'messages': messages,
        'item': item
    })
@login_required
def dashboard(request):

    if user.is_buyer:
        chat_partners = User.objects.filter(
            Q(received_messages__sender=user) | 
            Q(sent_messages__receiver=user)
        ).distinct().annotate(
            unread_messages=Count('received_messages', filter=Q(received_messages__is_read=False))
        )
    
    return render(request, 'accounts/buyer_dashboard.html', {

        'chat_partners': [(u, u.unread_messages) for u in chat_partners]
    })