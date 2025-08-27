from django.db import models

class WhatsAppBot(models.Model):
    name = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20)
    token = models.CharField(max_length=255)
    webhook_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Trigger(models.Model):
    bot = models.ForeignKey(WhatsAppBot, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=50)
    response = models.TextField()

    def __str__(self):
        return f"{self.keyword} → {self.response}"

class Conversation(models.Model):
    bot = models.ForeignKey(WhatsAppBot, on_delete=models.CASCADE)
    from_number = models.CharField(max_length=20)
    message = models.TextField()
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensagem de {self.from_number}"
