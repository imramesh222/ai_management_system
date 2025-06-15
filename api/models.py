# api/models.py
from django.db import models
from django.contrib.auth.models import User

class AIModel(models.Model):
    name = models.CharField(max_length=100, unique=True)

class AIPrompt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt_text = models.TextField()
    ai_model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Course(models.Model):
    title = models.CharField(max_length=200)

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollment')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollment')
