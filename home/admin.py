
from django.contrib import admin
from accounts.models import Item, User, Review
from user_messages.models import Message


admin.site.register(Item)
admin.site.register(User)
admin.site.register(Message)
admin.site.register(Review)