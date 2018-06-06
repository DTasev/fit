import datetime

from django.http import Http404
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import WorkoutSerializer
from workout.models import Workout, WorkoutExercise


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

    # def perform_create(self, serializer):
    @permission_classes((IsAuthenticated,))
    def create(self, request):
        workout_exercise_id = int(request.data["workoutexercise_id"])
        workout_exercise = WorkoutExercise.objects.get(pk=workout_exercise_id)
        if workout_exercise.workout.user == request.user:
            new_set = workout_exercise.sets.create(kgs=float(request.data["new_set"]["kgs"]),
                                                   reps=int(request.data["new_set"]["reps"]))
            return Response(data={"new_set": {"id": new_set.id}}, status=201)
        else:
            return Response(data={"message": "You don't own this."}, status=403)
