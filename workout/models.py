from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
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
    ARMS = "Arms"
    SHOULDERS = "Shoulders"
    LEGS = "Legs"
    BACK = "Back"
    CHEST = "Chest"

    MUSCLE_GROUPS = (
        (ARMS, 'Arms'),
        (SHOULDERS, 'Shoulders'),
        (LEGS, "Legs"),
        (BACK, "Back"),
        (CHEST, "Chest"),
    )
    muscle_group = models.CharField(max_length=200, choices=MUSCLE_GROUPS)
    name = models.CharField(max_length=200)
    is_compound = models.BooleanField(default=False)

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


class WorkoutDataCache(models.Model):
    workout = models.OneToOneField(Workout, on_delete=models.CASCADE, primary_key=True)
    kcals = models.FloatField("KCALs Burned from Workout", blank=True, default=None, null=True)

    START_KCALS = 1.75  # kcals per 1 min for 30kg
    NORMAL_KCALS_INCREMENT_PER_KG = 0.0583334  # increment per KG
    COMPOUND_KCALS_INCREMENT_PER_KG = 0.0833334  # increment per KG

    # (user_kgs - 30)*kg_kcals_increment + start_kcals

    def compute_kcals(self, workout: Workout, user: User):
        try:
            user_kgs = user.details.weight
        except ObjectDoesNotExist:
            user_kgs = 70

        compound_exercise_kcals = (user_kgs - 30) * self.COMPOUND_KCALS_INCREMENT_PER_KG + self.START_KCALS
        normal_exercise_kcals = (user_kgs - 30) * self.NORMAL_KCALS_INCREMENT_PER_KG + self.START_KCALS

        total_kcals = 0
        for set in workout.workoutexercise_set.all():
            if set.exercise.is_compound:
                total_kcals += set.sets.count() * compound_exercise_kcals
            else:
                total_kcals += set.sets.count() * normal_exercise_kcals

        self.kcals = round(total_kcals, 2)
        self.save()
