from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.views.generic.edit import UpdateView

from workout.models import WorkoutExercise, ExerciseSet


class UpdateSet(UpdateView):
    model = ExerciseSet
    template_name = 'sets/update.html'
    fields = ('kgs', 'reps')

    def get_success_url(self):
        return reverse('today:sets:add', kwargs={"pk": self.object.workout_exercise.pk})


def repeat_set(request, pk):
    e = WorkoutExercise.objects.get(id=pk)
    if request.method == "POST":
        last = e.sets.last()
        if last:
            last.pk = None
            last.save()
    return redirect(reverse('today:sets:add', kwargs={"pk": e.id}))


def del_set(request, pk):
    e = WorkoutExercise.objects.get(id=pk)
    if request.method == "POST":
        e.sets.last().delete()
    return redirect(reverse('today:sets:add', kwargs={"pk": e.id}))


# def add_set(request, pk):
#     e = WorkoutExercise.objects.get(id=pk)
#     if request.method == "GET":
#         last_set = e.sets.last()
#         return render(request, 'sets/edit.html',
#                       {"exercise": e, "prev_reps_value": getattr(last_set, "reps", None),
#                        "prev_kgs_value": getattr(last_set, "kgs", None),
#                        "last_set_time": getattr(last_set, "time", None)})
#     elif request.method == "POST":
#         # return error for missing KGs
#         if request.POST["kgs"] == "":
#             return render(request, 'sets/edit.html',
#                           {"exercise": e, "kgs_error": "KGs not specified", "prev_reps_value": request.POST["reps"]})
#         # return error for missing reps
#         elif request.POST["reps"] == "":
#             return render(request, 'sets/edit.html',
#                           {"exercise": e, "reps_error": "Reps not specified", "prev_kgs_value": request.POST["kgs"]})
#
#         e.sets.create(kgs=request.POST["kgs"], reps=request.POST["reps"], time=timezone.now())
#         return render(request, 'sets/edit.html',
#                       {"exercise": e, "prev_reps_value": request.POST["reps"], "prev_kgs_value": request.POST["kgs"]})
#

class AddSetView(generic.DetailView):
    model = WorkoutExercise

    def get_context_data(self, **kwargs):
        context = super(AddSetView, self).get_context_data(**kwargs)
        context["exercise_from_last_time"] = self.get_last_exercise(self.object, self.request)
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        latest_set = self.object.sets.last()

        #  TODO remove prev_reps_value and prev_kgs_value and just read them off of latest_set. make sure to pass it in the
        #  POST method though!
        return render(request, 'sets/edit.html',
                      {**context, "exercise": self.object,
                       "latest_set": latest_set})

    def get_last_exercise(self, e, request):
        past_exercises = WorkoutExercise.objects.filter(workout__user=request.user, exercise__name=e.exercise.name)
        exercise_from_last_time = None
        if len(past_exercises) > 1:
            # get the data for the last time the exercise was performed
            past_exercises = past_exercises[len(past_exercises) - 2]
            if past_exercises.sets.count() != 0:
                exercise_from_last_time = past_exercises
        return exercise_from_last_time

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)

        # return error for missing KGs
        if request.POST["kgs"] == "":
            return render(request, 'sets/edit.html',
                          {**context, "exercise": self.object, "kgs_error": "KGs not specified",
                           "prev_reps_value": request.POST["reps"]})
        # return error for missing reps
        elif request.POST["reps"] == "":
            return render(request, 'sets/edit.html',
                          {**context, "exercise": self.object, "reps_error": "Reps not specified",
                           "prev_kgs_value": request.POST["kgs"]})

        # both kgs and reps are present, check if the workout is started, and if not, start it
        workout = self.object.workout
        if not workout.start_time:
            workout.start_time = timezone.now()
            workout.save()

        latest_set = self.object.sets.create(kgs=request.POST["kgs"], reps=request.POST["reps"], time=timezone.now())
        return render(request, 'sets/edit.html',
                      {**context, "exercise": self.object,
                       "latest_set": latest_set})


def view_readonly_set(request, pk):
    e = WorkoutExercise.objects.get(id=pk)
    return render(request, 'sets/readonly.html', {"exercise": e})
