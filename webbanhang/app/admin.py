from django.contrib import admin
from .models import *

class MyModelBooks(Books):
    exclude = ('Time')

admin.site.register(MyModelBooks)
admin.site.register(Persons)
admin.site.register(Books)
admin.site.register(Carts)
admin.site.register(Categories)