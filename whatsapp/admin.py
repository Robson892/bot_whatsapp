from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import WhatsAppBot, Trigger, Conversation, User

# Registro do modelo User customizado
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Mostra campos importantes na lista de usuários
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

# Registro do modelo WhatsAppBot
@admin.register(WhatsAppBot)
class WhatsAppBotAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'phone_number', 'created_at')
    search_fields = ('name', 'phone_number', 'owner__username')
    list_filter = ('created_at',)
    raw_id_fields = ('owner',)

# Registro do modelo Trigger
@admin.register(Trigger)
class TriggerAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'bot', 'response')
    search_fields = ('keyword', 'response', 'bot__name')
    list_filter = ('bot',)

# Registro do modelo Conversation
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('from_number', 'bot', 'message', 'response', 'created_at')
    search_fields = ('from_number', 'message', 'response', 'bot__name')
    list_filter = ('bot', 'created_at')
