from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView
from .models import Interesting, Procedures, User, UserOrders, UserOrgs
from .forms import UserOrdersForm
from django.core.cache import cache
from django.core.exceptions import FieldError

class IndexPageView(TemplateView):
    template_name = 'indexpage/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'key':'value'}) #content to send to template
        return context


class FullBase(ListView):
    template_name = 'indexpage/base.html'
    paginate_by = 100
    queryset = cache.get('BASE')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Base'
        inter_list = Interesting.objects.filter(user=self.user_id)
        try:
            context['inter_list'] = inter_list[0].procedure.all().values_list('proc_number', flat=True)
        except IndexError:
            context['inter_list'] = None
        if not context['inter_list']:
            context['inter_list'] = True
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        self.user_id = request.user.id
        return super().get(self, request, *args, **kwargs)


class OldBase(ListView):
    template_name = 'indexpage/base.html'
    paginate_by = 100
    queryset = cache.get('OLD_BASE')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Old base'
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().get(self, request, *args, **kwargs)

class RecomendBase(ListView):
    template_name = 'indexpage/base.html'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Recomend'
        inter_list = Interesting.objects.filter(user=self.user_id)
        try:
            context['inter_list'] = inter_list[0].procedure.all().values_list('proc_number', flat=True)
        except IndexError:
            context['inter_list'] = None
        if not context['inter_list']:
            context['inter_list'] = True
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        self.queryset = cache.get('RECOMEND' + str(request.user.id))
        self.user_id = request.user.id
        return super().get(self, request, *args, **kwargs)


class InterestingBase(ListView):
    template_name = 'indexpage/base.html'
    model = Procedures
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Interesting'
        try:
            context['inter_list'] = self.queryset.values_list('proc_number', flat=True)
        except (IndexError, FieldError):
            context['inter_list'] = None
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            self.queryset = Interesting.objects.get(user=request.user.id).procedure.all().values('id', 'places__full_name', 'proc_number', 'law__full_name', 
                    'type_proc__full_name', 'orgs__full_name', 'orgs__inn', 'subject', 'date_start', 'date_end', 'date_proc', 'tradeplace__full_name', 
                    'stage__full_name', 'link', 'created_at', 'deal_count', 'region__full_name')
        except Exception as e:
            print('ERROR' + str(e))
            self.queryset = Interesting.objects.none()
        self.user_id = request.user.id
        return super().get(self, request, *args, **kwargs)

    @staticmethod
    def add_Interesting(request):
        if not request.user.is_authenticated:
            return redirect('login')
        print(request.GET)
        if not int(request.GET.get('value')):
            Interesting.objects.get(user=request.user.id).procedure.remove(Procedures.objects.get(pk=request.GET.get('pk')))
        else:
            try:
                inter = Interesting.objects.get(user=request.user.id)
            except Interesting.DoesNotExist:
                inter = Interesting(user=User.objects.get(pk=request.user.id)).save()
                inter = Interesting.objects.get(user=request.user.id)
            inter.procedure.add(*Procedures.objects.filter(pk=request.GET.get('pk')))
        return redirect(request.GET.get('next'))

class ProcedureView(ListView):
    template_name = 'indexpage/procedure.html'
    model = Procedures

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(kwargs)
        try:
            procedure = Procedures.objects.filter(proc_number=self.proc_number).values('id', 'places__full_name', 'proc_number', 'law__full_name', 
                    'type_proc__full_name', 'orgs__full_name', 'orgs__inn', 'subject', 'date_start', 'date_end', 'date_proc', 'tradeplace__full_name', 
                    'stage__full_name', 'link', 'created_at', 'deal_count', 'region__full_name')[0]
            context.update({'procedure':procedure, 'page_name':'Procedure'})
        except IndexError:
            print('nope')
        form = UserOrdersForm()
        form.fields['my_org'].queryset = Procedures.objects.all()[:10]
        context.update({'page_name':'Procedure', 'userordersform':form})
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        # print(kwargs['proc_num'], type(kwargs['proc_num']))
        self.proc_number = kwargs['proc_num']
        return super().get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(self.kwargs['proc_num'])
        try:
            orders = UserOrders.objects.get_or_create(user=User.objects.get(pk=request.user.id), 
                                            procedure=Procedures.objects.get(proc_number=self.kwargs['proc_num']),
                                            my_org = UserOrgs.objects.get(user=request.user.id))
        except UserOrders.DoesNotExist: 
            print('Nope')
        # orders.
        return redirect(request.path_info) 