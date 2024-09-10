from django.db import models
from django.contrib.auth.models import User, AbstractUser
import random
from phonenumber_field.modelfields import PhoneNumberField

class Chapter(models.Model):
    code = models.IntegerField()
    name_short = models.CharField(max_length=10)

    def __str__(self):
        return self.name_short

class CustomUser(AbstractUser):
    phone = PhoneNumberField()
    email = models.EmailField(max_length=100)

class Code(models.Model):
    number = models.CharField(max_length=5, blank=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)
    
    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]
        code_items = []
        for i in range(5):
            num = random.choice(number_list)
            code_items.append(num)
        code_string = "".join(str(item) for item in code_items)
        self.number = code_string

        super().save(*args, **kwargs)

# this is just a test comment to show github functionality