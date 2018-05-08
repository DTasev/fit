from django.shortcuts import render, redirect
from django.urls import reverse

from workout.models import WorkoutExercise, SPECIAL_EXERCISES_JOIN_CHARACTER


def repeat_set(request, pk):
    e = WorkoutExercise.objects.get(id=pk)
    if request.method == "POST":
        if e.sets != "":
            if SPECIAL_EXERCISES_JOIN_CHARACTER in e.sets:
                last_set = e.sets[:e.sets.rfind(SPECIAL_EXERCISES_JOIN_CHARACTER)]
            else:
                last_set = e.sets
            e.sets += SPECIAL_EXERCISES_JOIN_CHARACTER + last_set
            e.save()
    return redirect(reverse('today:add_set', kwargs={"pk": e.id}))


def del_set(request, pk):
    e = WorkoutExercise.objects.get(id=pk)
    if request.method == "POST":
        if SPECIAL_EXERCISES_JOIN_CHARACTER in e.sets:
            e.sets = e.sets[:e.sets.rfind(SPECIAL_EXERCISES_JOIN_CHARACTER)]
        else:
            e.sets = ""
        e.save()
    return redirect(reverse('today:add_set', kwargs={"pk": e.id}))


def add_set(request, pk):
    e = WorkoutExercise.objects.get(id=pk)
    if request.method == "GET":
        return render(request, 'today/sets.html', {"exercise": e})
    elif request.method == "POST":

        # return error for missing KGs
        if request.POST["kgs"] == "":
            return render(request, 'today/sets.html',
                          {"exercise": e, "kgs_error": "KGs not specified", "prev_reps_value": request.POST["reps"]})
        # return error for missing reps
        elif request.POST["reps"] == "":
            return render(request, 'today/sets.html',
                          {"exercise": e, "reps_error": "Reps not specified", "prev_kgs_value": request.POST["kgs"]})

        existing = e.sets
        if existing != "":
            existing += "{}{}x{}".format(SPECIAL_EXERCISES_JOIN_CHARACTER, request.POST["kgs"], request.POST["reps"])
        else:
            existing = "{}x{}".format(request.POST["kgs"], request.POST["reps"])
        e.sets = existing
        e.save()
        return render(request, 'today/sets.html', {"exercise": e})
