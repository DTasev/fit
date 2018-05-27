from django.contrib.auth.models import User
# Create your views here.
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from user_data.models import UserDetails


class ProfileDetail(generic.UpdateView):
    model = User
    template_name = 'user_profile/index.html'
    fields = ['first_name', 'last_name', 'email']

    # def get(self, request, *args, **kwargs):
    #     return render(request, self.template_name, context={"user": request.user})

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.id)

    def get_success_url(self):
        return reverse('user_profile:index', kwargs={"username": self.request.user.username})

    def form_valid(self, form):
        details, created = UserDetails.objects.get_or_create(user=self.object)
        details.weight = float(form.data["weight"])
        details.save()
        return redirect(reverse('user_profile:index', kwargs={"username": self.object.username}))
