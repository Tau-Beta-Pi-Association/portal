from django.contrib import admin
# from .models import Account
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Code

admin.site.register(CustomUser)
admin.site.register(Code)

