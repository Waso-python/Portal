from datetime import datetime, time
import random
import string
from django.shortcuts import redirect
from django.views.generic import ListView
from .models import (Interesting, Marketplaces, Procedures, Tradeplaces, User, UserOrders,
                     UserOrgs, UserContracts)
from .forms import UserContractsForm, UserOrdersForm, UserOrgsForm
from .modelforms import ProceduresForm
from django.core.cache import cache
from django.core.exceptions import FieldError
from mainportal.tasks import UpdateBase
import pytz


class FullBase(ListView):
    template_name = 'indexpage/base.html'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Все процедуры'
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
        self.queryset = cache.get('BASE')
        return super().get(self, request, *args, **kwargs)


class OldBase(ListView):
    template_name = 'indexpage/base.html'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Завершенные'
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        self.queryset = cache.get('OLD_BASE')
        return super().get(self, request, *args, **kwargs)


class RecomendBase(ListView):
    template_name = 'indexpage/base.html'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'Рекомендованные'
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
        recomend = cache.get('RECOMEND' + str(request.user.id))
        self.queryset = recomend if recomend else Procedures.objects.none()
        self.user_id = request.user.id
        return super().get(self, request, *args, **kwargs)


class InterestingBase(ListView):
    template_name = 'indexpage/work.html'
    model = Procedures
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'В Работе'
        try:
            context['inter_list'] = self.queryset.values_list('proc_number', flat=True)
        except (IndexError, FieldError):
            context['inter_list'] = None
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            self.queryset = Interesting.objects.get(user=request.user.id).procedure.all().values('id','places__full_name', 'proc_number', 'law__full_name',
                    'type_proc__full_name', 'orgs__full_name', 'orgs__inn', 'subject', 'date_start', 'date_end', 'date_proc', 'tradeplace__full_name',
                    'stage__full_name', 'link', 'created_at', 'deal_count', 'region__full_name', 'summ_proc')
        except Interesting.DoesNotExist as e:
            print('ERROR' + str(e))
            self.queryset = Interesting.objects.none()
        self.user_id = request.user.id
        return super().get(self, request, *args, **kwargs)

    @staticmethod
    def add_Interesting(request):
        if not request.user.is_authenticated:
            return redirect('login')
        # print(request.GET)
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


class ProcedureView(ListView, UpdateBase):
    template_name = 'indexpage/procedure.html'
    model = Procedures

    def get_general_context(self, **kwargs):
        context: dict = kwargs['sup']
        try:
            procedure = Procedures.objects.filter(proc_number=self.proc_number).values('id', 'places__full_name',
                    'proc_number', 'law__full_name', 'type_proc__full_name', 'orgs__full_name', 'orgs__inn',
                    'subject', 'date_start', 'date_end', 'date_proc', 'tradeplace__full_name',
                    'stage__full_name', 'link', 'created_at', 'deal_count', 'region__full_name')[0]
            context.update({'procedure': procedure})
        except IndexError as e:
            print('IndexError general_context', e)
        new_orders_form = UserOrdersForm()
        my_org_form = UserOrgsForm()
        my_org_form.fields['my_org'].queryset = self.user_orgs
        context.update({'page_name': 'Procedure',
                        'my_org_form': my_org_form,
                        'new_orders_form': new_orders_form,
                        'orders': self.user_orders})
        return context

    def get_personal_context(self, **kwargs):
        context: dict = kwargs['sup']
        try:
            procedure = Procedures.objects.filter(proc_number=self.proc_number)[0]
            form = ProceduresForm(procedure.get_form_dict())
            context.update({'form_procedure': form})
        except IndexError as e:
            print('IndexError personal_context', e)
        new_orders_form = UserOrdersForm()
        my_org_form = UserOrgsForm()
        my_org_form.fields['my_org'].queryset = self.user_orgs
        context.update({'page_name': 'Procedure',
                        'my_org_form': my_org_form,
                        'new_orders_form': new_orders_form,
                        'orders': self.user_orders})
        return context

    def get_context_data(self, **kwargs):
        procedure = Procedures.objects.get(proc_number=self.proc_number)
        if procedure.personal == False:
            return self.get_general_context(sup=super().get_context_data(**kwargs))
        else:
            return self.get_personal_context(sup=super().get_context_data(**kwargs))

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        self.proc_number = kwargs['proc_num']
        self.user_orgs = UserOrgs.objects.filter(user=request.user.id)
        self.user_orders = UserOrders.objects.filter(user=request.user.id,
                                                     procedure__proc_number=kwargs['proc_num']).order_by('-pk')
        # print(self.user_orders)
        return super().get(self, request, *args, **kwargs)

    def new_order(self, request):
        form_orders = UserOrdersForm(request.POST)
        if form_orders.is_valid():
            new_order = UserOrders(user=User.objects.get(pk=request.user.id),
                                   procedure=Procedures.objects
                                   .get(proc_number=self.kwargs['proc_num']),
                                   my_org=UserOrgs.objects.get(pk=int(request.POST['my_org'])),
                                   amount=form_orders.cleaned_data['amount'],
                                   comment=form_orders.cleaned_data['comment'],
                                   win='win' in request.POST)
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
            contract.contract_date = form.cleaned_data['contract_date']
            contract.deadline = form.cleaned_data['deadline']
            contract.day_to_shipping = form.cleaned_data['day_to_shipping']
            contract.comment = form.cleaned_data['comment']
            contract.save()

    def update_procedure(self, request):
        form = ProceduresForm(request.POST)
        print(self.kwargs['proc_num'])
        if form.is_valid():
            procedure = Procedures.objects.get(proc_number=self.kwargs['proc_num'])
            procedure.places = self.get_obj(Marketplaces ,form.cleaned_data['places'])
            procedure.law = form.cleaned_data['law']
            procedure.type_proc= form.cleaned_data['type_proc']
            procedure.orgs = self.get_org(f"{form.cleaned_data['orgs']}(:{form.cleaned_data['orgs_inn']}")
            procedure.subject = form.cleaned_data['subject']
            procedure.tradeplace = self.get_obj(Tradeplaces, form.cleaned_data['tradeplace'])
            procedure.stage = form.cleaned_data['stage']
            procedure.link = form.cleaned_data['link']
            procedure.summ_proc = form.cleaned_data['summ_proc']
            procedure.deal_count = form.cleaned_data['deal_count'] if form.cleaned_data['deal_count'] else 0
            procedure.region = form.cleaned_data['region']
            if form.cleaned_data['date_start']:
                procedure.date_start=pytz.timezone('Europe/Moscow').localize(datetime.combine(form.cleaned_data['date_start'],
                                        datetime.strptime(f"{form.cleaned_data['hours_start']}:{form.cleaned_data['minutes_start']}",
                                        '%H:%M').time()))
            if form.cleaned_data['date_end']:
                procedure.date_end=pytz.timezone('Europe/Moscow').localize(datetime.combine(form.cleaned_data['date_end'],
                                        datetime.strptime(f"{form.cleaned_data['hours_end']}:{form.cleaned_data['minutes_end']}",
                                        '%H:%M').time()))
            if form.cleaned_data['date_proc']:
                procedure.date_proc=pytz.timezone('Europe/Moscow').localize(datetime.combine(form.cleaned_data['date_proc'],
                                        datetime.strptime(f"{form.cleaned_data['hours_proc']}:{form.cleaned_data['minutes_proc']}",
                                        '%H:%M').time()))
        print(f'{procedure.date_start}\n{procedure.date_end}\n{procedure.date_proc}')
        procedure.save()


    def post(self, request, **kwargs):
        # print(self.kwargs['proc_num'])
        # print(request.POST)
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
        elif 'update_procedure' in request.POST:
            self.update_procedure(request)
        return redirect(request.path_info)


class CreateProcedure(ListView, UpdateBase):
    model = Procedures
    template_name = 'indexpage/create_procedure.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'form': ProceduresForm()})
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().get(self, request, *args, **kwargs)

    def post(self, request):
        # print(request.POST)
        form = ProceduresForm(request.POST)
        if form.is_valid():
            key = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
            procedure = Procedures(places=self.get_obj(Marketplaces, form.cleaned_data['places']),
                                   proc_number=f'{form.cleaned_data["proc_number"]}<-!->{key}',
                                   law=form.cleaned_data['law'],
                                   type_proc=form.cleaned_data['type_proc'],
                                   orgs=self.get_org(f"{form.cleaned_data['orgs']}(:{form.cleaned_data['orgs_inn']}"),
                                   subject=form.cleaned_data['subject'],
                                   tradeplace=self.get_obj(Tradeplaces, form.cleaned_data['tradeplace']),
                                   stage=form.cleaned_data['stage'],
                                   link=form.cleaned_data['link'],
                                   summ_proc = form.cleaned_data['summ_proc'],
                                   deal_count=form.cleaned_data['deal_count'] if form.cleaned_data['deal_count'] else 0,
                                   region=form.cleaned_data['region'],
                                   personal=True)
            if form.cleaned_data['date_start']:
                procedure.date_start=pytz.timezone('Europe/Moscow').localize(datetime.combine(form.cleaned_data['date_start'],
                                        datetime.strptime(f"{form.cleaned_data['hours_start']}:{form.cleaned_data['minutes_start']}",
                                        '%H:%M').time()))
            if form.cleaned_data['date_end']:
                procedure.date_end=pytz.timezone('Europe/Moscow').localize(datetime.combine(form.cleaned_data['date_end'],
                                        datetime.strptime(f"{form.cleaned_data['hours_end']}:{form.cleaned_data['minutes_end']}",
                                        '%H:%M').time()))
            if form.cleaned_data['date_proc']:
                procedure.date_proc=pytz.timezone('Europe/Moscow').localize(datetime.combine(form.cleaned_data['date_proc'],
                                        datetime.strptime(f"{form.cleaned_data['hours_proc']}:{form.cleaned_data['minutes_proc']}",
                                        '%H:%M').time()))
            print(f'{procedure.date_start}\n{procedure.date_end}\n{procedure.date_proc}')
            procedure.save()
            procedure = Procedures.objects.filter(id=procedure.id)
            try:
                inter = Interesting.objects.get(user=request.user.id)
            except Interesting.DoesNotExist:
                inter = Interesting.objects.create(user=User.objects.get(id=request.user.id))
            inter.procedure.add(*procedure)
        return redirect('interesting')
  