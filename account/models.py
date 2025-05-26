from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class UserAccount(models.Model):
    user_id=models.AutoField(primary_key=True)
    user_name=models.CharField(max_length=255)
    user_mailid=models.EmailField(unique=True)
    password=models.CharField(max_length=185)
    otp=models.CharField(max_length=6, blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(null=True, blank=True)
    phone_number=PhoneNumberField(null=True,blank=True)


    def __str__(self):
        return self.user_name



class Account(models.Model):
    name=models.CharField(max_length=255)
    phone_number=models.PhoneNumberField()
    address=models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name



















