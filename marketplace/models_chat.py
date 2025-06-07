from django.db import models
from django.contrib.auth.models import User

class ChatConversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="New Conversation")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.title} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class ChatMessage(models.Model):
    conversation = models.ForeignKey(ChatConversation, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField()
    response = models.TextField(blank=True)
    is_user = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    agent_used = models.CharField(max_length=50, blank=True)  # Which MCP agent was used
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{'User' if self.is_user else 'Assistant'}: {self.message[:50]}..."
