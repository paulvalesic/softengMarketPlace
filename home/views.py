from django.shortcuts import render,redirect, get_object_or_404
from accounts.models import Item, Review, User
from accounts.forms import ItemForm
from django.contrib.auth.decorators import login_required

def home(request):
    items = Item.objects.all()
    return render(request, 'home/home.html', {'items': items})

def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'home/item_detail.html', {'item': item})

def seller_profile(request, user_id):
    seller = get_object_or_404(User, id=user_id)
    reviews = Review.objects.filter(reviewed_user=seller)
    average_rating = seller.average_rating()  # Calls the User model method
    
    return render(request, 'home/seller_profile.html', {
        'seller': seller,
        'reviews': reviews,
        'average_rating': average_rating,
    })
    


@login_required
def update_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    # Verify ownership
    if item.seller != request.user:
        return redirect('home')
        
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_detail', item_id=item.id)
    else:
        form = ItemForm(instance=item)
    
    return render(request, 'home/update_item.html', {'form': form})