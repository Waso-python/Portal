from django.shortcuts import redirect
from django.views.generic import ListView, View, TemplateView
from .forms import KeysForm
from .models import ProfileUserModel

class ProfileView(ListView):
    template_name: str = 'usersProfile/profile.html'
    queryset = ProfileUserModel


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = KeysForm(initial=self.userkeys.get_format())
        context.update({'form':form})
        return context


    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        self.userkeys = ProfileUserModel.objects.get(user=request.user.id)
        return super().get(self, request, *args, **kwargs)

    def post(self, request):
        if request.method == 'POST':
            self.userkeys = ProfileUserModel.objects.get(user=request.user.id)
            self.userkeys.keys = {'places':request.POST['places'], 'law':request.POST['law'], 'type_proc':request.POST['type_proc'],
                             'orgs':request.POST['orgs'], 'subject':request.POST['subject'], 'region':request.POST['region']}
            self.userkeys.save()
        return redirect('profile')