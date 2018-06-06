from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from workout.models import Workout, WorkoutExercise, Exercise, ExerciseSet


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('name',)


class ExerciseSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseSet
        fields = ('id', 'kgs', 'reps')


class WorkoutExerciseSerializer(serializers.ModelSerializer):
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

    #     TODO finish this, need a separate section for "primary" and "secondary" exercises
    def get_primary_exercises(self, workout):
        primary = workout.primary()
        return WorkoutExerciseSerializer(primary, many=True).data

    def get_secondary_exercises(self, workout):
        secondary = workout.secondary()
        return WorkoutExerciseSerializer(secondary, many=True).data

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
