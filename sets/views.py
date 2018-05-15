from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import UpdateView

from workout.models import WorkoutExercise, ExerciseSet


class EditSet(UpdateView):
    model = ExerciseSet
    template_name = 'sets/edit.html'
    fields = ('kgs', 'reps')

    def get_success_url(self):
        return reverse('today:sets:add_set', kwargs={"pk": self.object.workout_exercise.pk})


def repeat_set(request, pk):
    e = WorkoutExercise.objects.get(id=pk)
    if request.method == "POST":
        last = e.sets.last()
        if last:
            last.pk = None
            last.save()
    return redirect(reverse('today:sets:add_set', kwargs={"pk": e.id}))


def del_set(request, pk):
    e = WorkoutExercise.objects.get(id=pk)
    if request.method == "POST":
        e.sets.last().delete()
    return redirect(reverse('today:sets:add_set', kwargs={"pk": e.id}))


def add_set(request, pk):
    e = WorkoutExercise.objects.get(id=pk)
    if request.method == "GET":
        last_set = e.sets.last()
        return render(request, 'today/sets_edit.html',
                      {"exercise": e, "prev_reps_value": getattr(last_set, "reps", None),
                       "prev_kgs_value": getattr(last_set, "kgs", None)})
    elif request.method == "POST":
        # return error for missing KGs
        if request.POST["kgs"] == "":
            return render(request, 'today/sets_edit.html',
                          {"exercise": e, "kgs_error": "KGs not specified", "prev_reps_value": request.POST["reps"]})
        # return error for missing reps
        elif request.POST["reps"] == "":
            return render(request, 'today/sets_edit.html',
                          {"exercise": e, "reps_error": "Reps not specified", "prev_kgs_value": request.POST["kgs"]})

        e.sets.create(kgs=request.POST["kgs"], reps=request.POST["reps"])
        return render(request, 'today/sets_edit.html',
                      {"exercise": e, "prev_reps_value": request.POST["reps"], "prev_kgs_value": request.POST["kgs"]})


def view_readonly_set(request, pk):
    e = WorkoutExercise.objects.get(id=pk)
    return render(request, 'today/sets_readonly.html', {"exercise": e})
