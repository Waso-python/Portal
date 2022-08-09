from django.shortcuts import render, redirect
from django.views.generic import ListView

def temp(request):
    return render(request, 'usersProfile/profile.html', {}) 

class ProfileView(ListView):
    template_name: str = 'usersProfile/profile.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        self.user_id = request.user.id
        return super().get(self, request, *args, **kwargs)