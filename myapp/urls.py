from django.urls import path
from .views import RandomExerciseView

urlpatterns = [
    path('random-exercises/', RandomExerciseView.as_view(), name='random_exercises'),
]
