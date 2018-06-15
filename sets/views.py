from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import UpdateView

from common.sets.add_set import add_set_routine, get_last_exercise
from common.sets.add_set_data import AddSetData
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


# def del_set(request, pk):
#     e = WorkoutExercise.objects.get(id=pk)
#     if request.method == "POST":
#         e.sets.last().delete()
#     return redirect(reverse('today:sets:add', kwargs={"pk": e.id}))

# Create your views here.
class DeleteSet(generic.DeleteView):
    model = ExerciseSet

    def post(self, request, *args, **kwargs):
        obj = super(DeleteSet, self).get_object()
        if not obj.workout_exercise.workout.user == self.request.user:
            # Raise 404 to not show the user that the entry exists
            return HttpResponseForbidden()

        obj.delete()
        return HttpResponse('Entry deleted successfully')


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
        context["exercise_from_last_time"] = get_last_exercise(self.object, self.request.user)
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        sets_so_far = self.object.sets.all()

        # we can only perform this calculation if 2 or more sets are present
        len_of_sets = len(sets_so_far)
        if len_of_sets > 1:
            latest_set = sets_so_far[len_of_sets - 1]
            penultimate_set = sets_so_far[len_of_sets - 2]
            set_kg_difference = latest_set.kgs - penultimate_set.kgs
            context["set_kg_difference"] = set_kg_difference
            context["latest_set"] = latest_set
        elif len_of_sets == 1:
            latest_set = sets_so_far[0]
            context["latest_set"] = latest_set

        return render(request, 'sets/edit.html',
                      {**context, "exercise": self.object})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)

        # return error for missing KGs
        if request.POST["kgs"] == "":
            return render(request, 'sets/edit.html',
                          {**context, "exercise": self.object, "kgs_error": "KGs not specified",
                           "prev_reps_value": request.POST["reps"]}, status=400)
        # return error for missing reps
        elif request.POST["reps"] == "":
            return render(request, 'sets/edit.html',
                          {**context, "exercise": self.object, "reps_error": "Reps not specified",
                           "prev_kgs_value": request.POST["kgs"]}, status=400)

        # both kgs and reps are present, check if the workout is started, and if not, start it
        data = AddSetData(request.POST["kgs"], request.POST["reps"])
        new_set = add_set_routine(self.object, data)

        return redirect(
            reverse('today:sets:add', kwargs={"pk": self.object.id}),
            kwargs={**context, "exercise": self.object, "latest_set": new_set})


def view_readonly_set(request, pk):
    e = WorkoutExercise.objects.get(id=pk)
    return render(request, 'sets/readonly.html', {"exercise": e})
