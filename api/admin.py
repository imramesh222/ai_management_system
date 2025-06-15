from django.contrib import admin
from .models import AIModel, AIPrompt

class AIModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class AIPromptAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'prompt_text', 'ai_model', 'created_at')

admin.site.register(AIModel, AIModelAdmin)
admin.site.register(AIPrompt, AIPromptAdmin)
