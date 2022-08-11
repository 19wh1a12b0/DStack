from statistics import mode
from django.db import models

# Create your models here.
class User(models.Model):
    WalletAddress = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.WalletAddress

class QuestionM(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    hash = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits = 5,decimal_places = 3)
    isActive = models.BooleanField(default=False)
    isFree = models.BooleanField(default=False)

    def __str__(self):
        return self.hash
    

class Comments(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    question =  models.ForeignKey(QuestionM,on_delete=models.CASCADE)
    data = models.CharField(max_length=500, null=True, blank=True)
    won = models.BooleanField(default=False)
    isActive = models.BooleanField(default=False)

    def __str__(self):
        return self.user.WalletAddress
