from django.urls import path
from .views import RegisterView, LoginView, AIPromptView, AIPromptListView, ActiveUsersWithCourseCountView, UserListView, MostFrequentVowelConsonantView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),

    # AI-related endpoints
    path('prompts/', AIPromptView.as_view()),
    path('prompts/list/', AIPromptListView.as_view()),
    path('active-users/', ActiveUsersWithCourseCountView.as_view()),
    path('users/', UserListView.as_view()),
    path('most-frequent-vowel-consonant/', MostFrequentVowelConsonantView.as_view()),

]