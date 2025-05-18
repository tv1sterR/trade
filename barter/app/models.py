from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=50)
    condition = models.CharField(max_length=50, choices=[('new', 'Новый'), ('used', 'БУ')])
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class ExchangeOffer(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    post_sender = models.ForeignKey(Product, related_name="sent_offers", on_delete=models.CASCADE)
    post_receiver = models.ForeignKey(Product, related_name="received_offers", on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=20,
                            choices=[('pending', 'Ожидает'), ('accepted', 'Принят'), ('declined', 'Отклонен')],
                            default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Обмен {self.post_sender.title} - {self.post_receiver.title} ({self.get_status_display()})"