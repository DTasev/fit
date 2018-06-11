import datetime

from django.http import Http404
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import WorkoutSerializer
from common.sets.add_set import add_set_routine
from common.sets.add_set_data import AddSetData
from workout.models import Workout, WorkoutExercise, ExerciseSet


class WorkoutViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)

    def retrieve(self, request, pk=None):
        try:
            serialized = WorkoutSerializer(
                Workout.objects.get(date=datetime.date.today(), user=self.request.user))
            return Response(serialized.data)
        except Workout.DoesNotExist:
            raise Http404


class AddNewSet(viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)

    @permission_classes((IsAuthenticated,))
    def create(self, request):
        workout_exercise_id = int(request.data["workoutexercise_id"])
        workout_exercise = WorkoutExercise.objects.get(pk=workout_exercise_id)
        if workout_exercise.workout.user == request.user:
            data = AddSetData(kgs=float(request.data["new_set"]["kgs"]), reps=int(request.data["new_set"]["reps"]))
            new_set = add_set_routine(workout_exercise, data)
            return Response(data={"new_set": {"id": new_set.id, "time": new_set.time}}, status=201)
        else:
            return Response(data={"message": "You don't own this."}, status=403)


class DeleteSet(viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)

    @permission_classes((IsAuthenticated,))
    def destroy(self, request, pk=None):
        try:
            exercise_set = ExerciseSet.objects.get(pk=pk)
        except ExerciseSet.DoesNotExist:
            return Response(data={"message": "Not Found"}, status=404)

        if exercise_set.workout_exercise.workout.user == request.user:
            exercise_set.delete()
            return Response(data={"message": "Deleted"}, status=200)
        else:
            return Response(data={"message": "You don't own this."}, status=403)
