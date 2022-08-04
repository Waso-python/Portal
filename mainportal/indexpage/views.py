from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView
from .models import *
from django.core.cache import cache

class IndexPageView(TemplateView):
    template_name = 'indexpage/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'key':'value'}) #content to send to template
        return context


class FullBase(ListView):
    template_name = 'indexpage/updatebase.html'
    paginate_by = 100
    queryset = cache.get('BASE')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inter_list = Interesting.objects.filter(user=self.user_id)
        print(bool(inter_list))
        context['inter_list'] = inter_list[0].procedure.all().values_list('proc_number', flat=True)
        if not context['inter_list']:
            context['inter_list'] = True
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        self.user_id = request.user.id
        return super().get(self, request, *args, **kwargs)


class OldBase(ListView):
    template_name = 'indexpage/updatebase.html'
    paginate_by = 100
    queryset = cache.get('OLD_BASE')

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().get(self, request, *args, **kwargs)


class InterestingBase(ListView):
    template_name = 'indexpage/updatebase.html'
    model = Procedures
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inter_list = Interesting.objects.filter(user=self.user_id)
        context['inter_list'] = inter_list[0].procedure.all().values_list('proc_number', flat=True)
        return context

    def get(self, request, *args, **kwargs):
        print(str(request.user.id) + 'inter' + str(request.GET['page'] if len(request.GET) != 0 else '1'))
        page = cache.get(str(request.user.id) + 'inter' + str(request.GET['page'] if len(request.GET) != 0 else '1'))
        if page:
            return page
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            self.queryset = Interesting.objects.get(user=request.user.id).procedure.all()
        except Exception as e:
            print('ERROR' + e)
            self.queryset = Interesting.objects.none()
        print(self.queryset)
        self.user_id = request.user.id
        return super().get(self, request, *args, **kwargs)
        page = super().get(self, request, *args, **kwargs).render()
        cache.set(str(request.GET['page'] if len(request.GET) != 0 else '1'), page)
        return page


def add_Interesting(request):
    if not request.user.is_authenticated:
        return redirect('login')
    print(request.GET)
    if not int(request.GET.get('value')):
        Interesting.objects.get(user=request.user.id).procedure.remove(Procedures.objects.get(pk=request.GET.get('pk')))
        # cache.set('???', None)
    else:
        inter = Interesting.objects.get(user=request.user.id)
        inter.procedure.add(*Procedures.objects.filter(pk=request.GET.get('pk')))
        # cache.set(str('???' if len(request.GET) != 0 else '1'), None)
    return redirect(request.GET.get('next'))