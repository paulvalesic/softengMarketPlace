from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    is_buyer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    token_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Dodaj related_name argumente kako bi se izbjegao sukob s ugrađenim User modelom
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="accounts_user_groups",  # Dodaj related_name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="accounts_user_permissions",  # Dodaj related_name
        related_query_name="user",
    )

    def __str__(self):
        return self.username
    
    def average_rating(self):
        reviews = Review.objects.filter(reviewed_user=self)
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg']
        return None
    
class Item(models.Model):
    CATEGORY_CHOICES = [
        ('ELECTRONICS', 'Electronics'),
        ('CLOTHING', 'Clothing'),
        ('BOOKS', 'Books'),
        ('HOME', 'Home'),
        ('OTHER', 'Other'),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    image_url = models.URLField()
    quantity = models.PositiveIntegerField(default=1)  # Dodajte količinu
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # Metoda za provjeru je li artikl rasprodan
    def is_sold_out(self):
        return self.quantity == 0

# accounts/models.py
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Completed', 'Completed'),
    ]

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(null=True, blank=True)  # Dodajte polje za ocjenu
    review = models.TextField(null=True, blank=True)  # Dodajte polje za komentar

    def __str__(self):
        return f"{self.buyer.username} - {self.item.title}"
    
    def confirm_order(self):
        if self.status == 'Pending':
            self.status = 'Confirmed'
            self.save()

# accounts/models.py
class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_review')  # Novi red
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)