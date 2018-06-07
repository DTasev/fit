from django.utils import timezone

from workout.models import WorkoutExercise


def add_set_routine(obj: WorkoutExercise, request):
    workout = obj.workout
    if not workout.start_time:
        workout.start_time = timezone.now()
        workout.save()
    latest_set = obj.sets.create(kgs=request.POST["kgs"], reps=request.POST["reps"], time=timezone.now())
    return latest_set
