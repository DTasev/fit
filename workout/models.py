from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

SPECIAL_EXERCISES_JOIN_CHARACTER = "|"


# Create your models here.
class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField("Date")
    primary_muscle_group = models.CharField(max_length=50)
    secondary_muscle_group = models.CharField(max_length=50)
    completed = models.BooleanField("Completed", default=False)

    start_time = models.DateTimeField("Start time of Workout", null=True, default=None)
    end_time = models.DateTimeField("End time of Workout", null=True, default=None)

    def primary(self):
        return self.workoutexercise_set.filter(exercise__muscle_group=self.primary_muscle_group)

    def secondary(self):
        return self.workoutexercise_set.filter(exercise__muscle_group=self.secondary_muscle_group)

    def duration(self):
        if not self.start_time:
            return ""
        if not self.end_time:
            return str(timezone.now() - self.start_time)[:7]
        return "Duration: " + str(self.end_time - self.start_time)[:7]

    class Meta:
        ordering = ["-date"]


class Exercise(models.Model):
    muscle_group = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    # format: "30x12|30x10"
    old_sets = models.TextField(default="")

    def __str__(self):
        return str(self.exercise)

    def sets_string(self):
        sets_string = ""
        for set in self.sets.all():
            sets_string += " {} KG x {} reps\n".format(set.kgs, set.reps)

        # removes the trailing coma
        return sets_string[:-1]

    def sets_js_array(self):
        sets_string = "["
        for set in self.sets.all():
            sets_string += '{{ "kgs": {}, "reps": {} }},'.format(set.kgs, set.reps)

        # removes the trailing coma
        return sets_string + "]"

    def sets_table(self):
        """
        TODO this should probably be in a partial rather than the model
        :return:
        """
        sets_table = """
        <table class="table table-sm"><thead><tr><th>Set</th><th>KGs</th><th>Reps</th></tr></thead>
        <tbody>{}</tbody></table>"""

        sets_rows = ""
        for i, set_data in enumerate(self.sets.all(), start=1):
            sets_rows += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(i, set_data.kgs, set_data.reps)

        return sets_table.format(sets_rows)


class ExerciseSet(models.Model):
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE, related_name="sets")
    reps = models.IntegerField()
    kgs = models.FloatField()
