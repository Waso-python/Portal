from django.shortcuts import redirect
from django.urls import is_valid_path
from django.views.generic import TemplateView, ListView
from .models import Interesting, Procedures, User, UserOrders, UserOrgs, UserContracts
from .forms import UserContractsForm, UserOrdersForm, UserOrgsForm
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
        try:
            procedure = Procedures.objects.filter(proc_number=self.proc_number).values('id', 'places__full_name', 'proc_number', 'law__full_name', 
                    'type_proc__full_name', 'orgs__full_name', 'orgs__inn', 'subject', 'date_start', 'date_end', 'date_proc', 'tradeplace__full_name', 
                    'stage__full_name', 'link', 'created_at', 'deal_count', 'region__full_name')[0]
            context.update({'procedure':procedure, 'page_name':'Procedure'})
        except IndexError:
            print('nope')
        new_orders_form = UserOrdersForm()
        my_org_form = UserOrgsForm()
        my_org_form.fields['my_org'].queryset = self.user_orgs
        context.update({'page_name':'Procedure',
                        'my_org_form':my_org_form,
                        'new_orders_form':new_orders_form,
                        'orders':self.user_orders})
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        # print(kwargs['proc_num'], type(kwargs['proc_num']))
        self.proc_number = kwargs['proc_num']
        self.user_orgs = UserOrgs.objects.filter(user=request.user.id)
        self.user_orders = UserOrders.objects.filter(user=request.user.id,
                                                     procedure=Procedures.objects.get(proc_number=int(kwargs['proc_num'])))
        # print(self.user_orders)
        return super().get(self, request, *args, **kwargs)

    def new_order(self, request):
        form_orders = UserOrdersForm(request.POST)
        print(form_orders, type(form_orders) )
        if form_orders.is_valid():
            new_order = UserOrders(user=User.objects.get(pk=request.user.id),
                                    procedure=Procedures.objects.get(proc_number=int(self.kwargs['proc_num'])),
                                    my_org=UserOrgs.objects.get(pk=int(request.POST['my_org'])),
                                    amount=form_orders.cleaned_data['amount'],
                                    comment=form_orders.cleaned_data['comment'],
                                    win='win'in request.POST)
            new_order.save()
            UserContracts(order=new_order).save()

    def delete_order(self, order_id, user_id):
        UserOrders.objects.filter(pk=order_id, user=user_id).delete()

    def update_order(self, request):
        form = UserOrdersForm(request.POST)
        if form.is_valid():
            order = UserOrders.objects.get(pk=int(request.POST['update']),
                                        user=request.user.id)
            order.amount = form.cleaned_data['amount']
            order.comment = form.cleaned_data['comment']
            order.win = 'win' in request.POST
            order.save()
    
    def update_contract(self, request):
        contract = UserContracts.objects.get(order=UserOrders.objects.get(pk=int(request.POST['update_contract']),
                                                                          user=request.user.id))
        contract.contract_num = request.POST['contract_num']
        form = UserContractsForm(request.POST)
        if form.is_valid(): 
            contract.contract_date= form.cleaned_data['contract_date']
            contract.deadline = form.cleaned_data['deadline']
            contract.day_to_shipping = form.cleaned_data['day_to_shipping']
            contract.comment = form.cleaned_data['comment']
            contract.save()

    def post(self, request, *args, **kwargs):
        print(self.kwargs['proc_num'])
        print(request.POST)
        if 'add' in request.POST:
            self.new_order(request)
            print('ADD')
        elif 'update' in request.POST:
            self.update_order(request)
            print('UPDATE')
        elif 'delete' in request.POST:
            self.delete_order(int(request.POST['delete']), request.user.id)
            print('DELETE')
        elif 'update_contract' in request.POST:
            self.update_contract(request)
        return redirect(request.path_info)