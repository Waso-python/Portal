from ast import Delete
from django.shortcuts import redirect
from django.views.generic import ListView
from .forms import forms, KeysForm, UserOrgsForm
from .models import ProfileUserModel
from indexpage.models import UserOrgs, User
from mainportal.tasks import cache_recomend

class ProfileView(ListView):
    template_name: str = 'usersProfile/profile.html'
    queryset = ProfileUserModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_keys = KeysForm(initial=self.userkeys.get_format())
        form_orgs = UserOrgsForm()
        form_orgs.fields['old'].queryset = self.user_orgs
        context.update({'form_keys':form_keys, 'form_orgs':form_orgs})
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        self.userkeys = ProfileUserModel.objects.get(user=request.user.id)
        self.user_orgs = UserOrgs.objects.filter(user=request.user.id)
        return super().get(self, request, *args, **kwargs)

    def change_keys(self, request):
        form = KeysForm(request.POST)
        if form.is_valid():
            userkeys = ProfileUserModel.objects.get(user=request.user.id)
            userkeys.keys = {'places':form.cleaned_data['places'],
                             'law':form.cleaned_data['law'],
                             'type_proc':form.cleaned_data['type_proc'],
                             'orgs':form.cleaned_data['orgs'],
                             'inn':form.cleaned_data['inn'],
                             'subject':form.cleaned_data['subject'],
                             'region':form.cleaned_data['region']}
            userkeys.save()
            cache_recomend.delay(request.user.id)

    def change_orgs(self, request):
        
        if request.POST['form_orgs'] == 'save' and request.POST['new']:
            form = UserOrgsForm(request.POST)
            if form.is_valid():
                UserOrgs(name=form.cleaned_data['new'], user=User.objects.get(pk=request.user.id)).save()
        elif request.POST['form_orgs'] == 'delete' and request.POST['old']:
            delete_org = UserOrgs.objects.get(pk=int(request.POST['old']), user__pk=request.user.id)
            print(delete_org)
            delete_org.delete()

    def post(self, request):
        if 'form_keys' in request.POST:
            self.change_keys(request)
        elif 'form_orgs' in request.POST:
            self.change_orgs(request)
        print(request.POST)
        return redirect('profile')