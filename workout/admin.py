from django.contrib import admin

from .models import Exercise


# Register your models here.

class ExerciseAdmin(admin.ModelAdmin):
    model = Exercise


admin.site.register(Exercise, ExerciseAdmin)
