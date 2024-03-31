from django.http import JsonResponse
from django.views import View
import pandas as pd
import random
from django.conf import settings


# Load the dataset
# data = pd.read_csv('gym-exercise-data.csv')
data_file_path = settings.BASE_DIR / 'myapp' / 'gym-exercise-data.csv'
data = pd.read_csv(data_file_path)


def random_exercise_generator(type_filter=None, level_filter=None, n=15):
    """
    Generate a random exercise based on type and level filters.
    If no filters are provided, a random exercise from the entire dataset is selected.
    """
    if type_filter:
        data_filtered = data[data['Type'] == type_filter]
    else:
        data_filtered = data

    if level_filter:
        data_filtered = data_filtered[data_filtered['Level'] == level_filter]

    if data_filtered.empty:
        return None

    random_exercises = data_filtered.sample(n=n)

    return random_exercises

class RandomExerciseView(View):
    def get(self, request):
        type_filter = request.GET.get('type', None)
        level_filter = request.GET.get('level', None)
        n = int(request.GET.get('n', 15))

        random_exercises = random_exercise_generator(type_filter, level_filter, n)

        if random_exercises is not None:
            exercises_list = [{'title': row['Title']} for index, row in random_exercises.iterrows()]
            return JsonResponse({'exercises': exercises_list})
        else:
            return JsonResponse({'error': 'No exercises match the specified filters.'}, status=400)
