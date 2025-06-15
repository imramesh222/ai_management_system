from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, AIPromptSerializer, UserListSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Count
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from typing import List
import string
from django.contrib.auth.models import User
from api.models import Course, Enrollment
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"detail": "Please use POST to register a new user."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=400)
        user = authenticate(username=user.username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Invalid credentials"}, status=400)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

class AIPromptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AIPromptSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            prompt = serializer.save()
            return Response({
                "message": "Prompt saved successfully",
                "prompt_id": prompt.id
            }, status=201)
        return Response(serializer.errors, status=400)

class AIPromptListView(ListAPIView):
    serializer_class = AIPromptSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['created_at', 'ai_model__name']

class ActiveUsersWithCourseCountView(APIView):
    def get(self, request):
        users = User.objects.annotate(course_count=Count('enrollment')) \
            .filter(course_count__gte=2) \
            .values('username', 'course_count') \
            .order_by('-course_count')
        return Response(list(users))

def most_frequent_vowel_and_consonant(s: str) -> List[str]:
    s = s.lower()
    vowels = 'aeiou'
    freq_vowel = {}
    freq_consonant = {}
    for ch in s:
        if ch in string.ascii_lowercase:
            if ch in vowels:
                freq_vowel[ch] = freq_vowel.get(ch, 0) + 1
            else:
                freq_consonant[ch] = freq_consonant.get(ch, 0) + 1
    most_vowel = min(
        (k for k, v in freq_vowel.items() if v == max(freq_vowel.values(), default=0)),
        default='',
    ) if freq_vowel else ''
    most_consonant = min(
        (k for k, v in freq_consonant.items() if v == max(freq_consonant.values(), default=0)),
        default='',
    ) if freq_consonant else ''
    return [most_vowel, most_consonant]

class MostFrequentVowelConsonantView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        s = request.data.get('text', '')
        result = most_frequent_vowel_and_consonant(s)
        return Response({'most_frequent_vowel': result[0], 'most_frequent_consonant': result[1]})

class TopEnrolledCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from django.db.models import Count
        from api.models import Course
        top_courses = Course.objects.annotate(user_count=Count('enrollment')).order_by('-user_count')[:5]
        data = [
            {
                'id': course.id,
                'title': course.title,
                'user_count': course.user_count
            } for course in top_courses
        ]
        return Response(data)

# ORM queries for reference and shell use

# Users registered in last 7 days
seven_days_ago = timezone.now() - timedelta(days=7)
recent_users = User.objects.filter(date_joined__gte=seven_days_ago)

# Count users enrolled in each course
users_per_course = Course.objects.annotate(user_count=Count('enrollment'))

# Users who haven’t logged in for 30 days
thirty_days_ago = timezone.now() - timedelta(days=30)
inactive_users = User.objects.filter(last_login__lte=thirty_days_ago)

# Top 5 most enrolled courses
most_enrolled_courses = Course.objects.annotate(user_count=Count('enrollment')).order_by('-user_count')[:5]

# Students and their course titles
student_courses = Enrollment.objects.select_related('user', 'course')

# Users enrolled in more than 3 courses
users_gt3 = User.objects.annotate(course_count=Count('enrollment')).filter(course_count__gt=3)

# Average enrollments per course
avg_enrollments = Course.objects.annotate(enrollment_count=Count('enrollment')).aggregate(avg=Avg('enrollment_count'))
