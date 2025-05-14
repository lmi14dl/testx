from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Portfolio(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    video = models.FileField(upload_to='upload/videos', blank=True, null=True)

    def __str__(self):
        return self.title

class PortfolioImage(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='upload/images')
    
    def __str__(self):
        return f"Image for {self.portfolio.title}"
    
class ContactRequest(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    source = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"
    
    class Meta:
        ordering = ['-created_at']


class WebsiteOrderFormRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    design_type = models.CharField(max_length=100, choices=[
        ('WordPress', 'WordPress'),
        ('Coding', 'Coding'),
    ])
    price = models.IntegerField(default=100)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TelegramBotOrderFormRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title