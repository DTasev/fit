from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from common.sets.add_set import get_last_exercise
from workout.models import Workout, WorkoutExercise, Exercise, ExerciseSet


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('name',)


class ExerciseSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseSet
        fields = ('id', 'kgs', 'reps')


class WorkoutExerciseWithHistorySerializer(serializers.ModelSerializer):
    """
    Serialise a WorkoutExercise, and retrieve a previous instance of the exercise (if present)
    """
    exercise = ExerciseSerializer()
    sets = ExerciseSetSerializer(many=True)
    exercise_from_last_time = SerializerMethodField()

    class Meta:
        model = WorkoutExercise
        fields = ('id', 'exercise', 'sets', 'exercise_from_last_time')

    def get_exercise_from_last_time(self, workout_exercise):
        exercise_from_last_time = get_last_exercise(workout_exercise, workout_exercise.workout.user)
        if exercise_from_last_time:
            return WorkoutExerciseSerializer(exercise_from_last_time).data
        else:
            return None


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    """
    Serialise a WorkoutExercise. No history is retrieved for it
    """
    exercise = ExerciseSerializer()
    sets = ExerciseSetSerializer(many=True)

    class Meta:
        model = WorkoutExercise
        fields = ('id', 'exercise', 'sets')


# class WorkoutSerializer(serializers.ModelSerializer):
#     workoutexercise_set = WorkoutExerciseSerializer(many=True)
#
#     class Meta:
#         model = Workout
#         fields = ('id', 'date',
#                   'primary_muscle_group', 'secondary_muscle_group',
#                   'completed', 'start_time', 'end_time', 'workoutexercise_set')

class WorkoutSerializer(serializers.ModelSerializer):
    primary_exercises = SerializerMethodField()
    secondary_exercises = SerializerMethodField()

    class Meta:
        model = Workout
        fields = ('id', 'date',
                  'primary_muscle_group', 'secondary_muscle_group',
                  'completed', 'start_time', 'end_time', 'primary_exercises', 'secondary_exercises')

    def get_primary_exercises(self, workout):
        primary = workout.primary()
        return WorkoutExerciseWithHistorySerializer(primary, many=True).data

    def get_secondary_exercises(self, workout):
        secondary = workout.secondary()
        return WorkoutExerciseWithHistorySerializer(secondary, many=True).data

# class DayTaskSerializer(serializers.ModelSerializer):
#     task = TaskSerializer()
#
#     class Meta:
#         model = DayTask
#         fields = ('id', 'task', 'allocated_time', 'completed', 'period')
#
#
# class DayPlanSerializer(serializers.ModelSerializer):
#     """
#     DayPlan serializer will only send the DayTasks that are NOT completed.
#     """
#     # tasks = DayTaskSerializer(many=True)
#     tasks = SerializerMethodField()
#
#     class Meta:
#         model = DayPlan
#         fields = ('date', 'duration', 'tasks')
#
#     def get_tasks(self, dayplan):
#         tasks = DayTask.objects.filter(completed=False, day=dayplan)
#         return DayTaskSerializer(tasks, many=True).data
