from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from .models import Conversation, Message

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at', 'message_count')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title',)
    readonly_fields = ('created_at', 'updated_at')
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('chat/', self.admin_site.admin_view(self.chat_view), name='ai_assistant_chat'),
        ]
        return custom_urls + urls

    def chat_view(self, request):
        from django.shortcuts import render
        from .models import Conversation
        from django.contrib.auth.models import User
        
        # Get or create a default conversation for admin use
        admin_user = request.user if request.user.is_authenticated else User.objects.filter(is_superuser=True).first()
        
        conversation, created = Conversation.objects.get_or_create(
            user=admin_user,
            title="AI Assistant Chat",
            defaults={'title': "AI Assistant Chat", 'user': admin_user}
        )
        
        # Get messages for this conversation
        messages = conversation.messages.all().order_by('timestamp')
        
        return render(request, 'admin/ai_assistant/chat.html', {
            'title': 'AI Assistant Chat',
            'has_permission': True,
            'active_conversation': conversation,
            'current_conversation': conversation,
            'messages': messages,
            'conversations': Conversation.objects.filter(user=admin_user).order_by('-updated_at'),
        })

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'role', 'content_preview', 'timestamp')
    list_filter = ('role', 'timestamp', 'conversation')
    search_fields = ('content', 'conversation__title')
    readonly_fields = ('timestamp',)
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'


# Custom admin site modifications to add AI Assistant link
from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse

# Remove the problematic monkey patching and custom admin site
# The AI Assistant will be accessible through the admin URLs directly
