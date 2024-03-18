
from django.contrib import admin
from .models import Customer, User, bill, collection, inquiry, items

admin.site.register(User)
admin.site.register(items)
admin.site.register(Customer)
admin.site.register(bill)
admin.site.register(inquiry)
admin.site.register(collection)
