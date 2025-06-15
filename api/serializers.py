from rest_framework import serializers
from django.contrib.auth.models import User
from .models import AIPrompt, AIModel
from rest_framework.serializers import ModelSerializer


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class AIPromptSerializer(serializers.ModelSerializer):
    ai_model = serializers.SlugRelatedField(
        slug_field='name', queryset=AIModel.objects.all()
    )

    class Meta:
        model = AIPrompt
        fields = ['id', 'prompt_text', 'ai_model', 'response_text', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        return AIPrompt.objects.create(user=user, **validated_data)