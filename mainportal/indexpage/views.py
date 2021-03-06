from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView, ListView
from .models import *
from datetime import datetime
import pytz
import time
from asgiref.sync import sync_to_async, async_to_sync

class IndexPageView(TemplateView):
    template_name = 'indexpage/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'key':'value'}) #content to send to template
        return context

class UpdateBase(View):
    template_name = 'indexpage/updatebase.html'


    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.rawdata = None

    def get(self, request):
        async_to_sync(self.fillBase)()
        return redirect('base')

    def get_obj(self, model, value):
        try:
            obj = model.objects.get(full_name=value)
        except:
            obj = model.objects.create(full_name=value)
        return obj

    def get_org(self, partner):
        org_inn = ''.join([i if i.isdigit() else '' for i in partner.split(':')[1]])
        try:
            obj = Orgs.objects.get(inn=org_inn)
        except:
            org_name = partner.split('(')[0]
            obj = Orgs.objects.create(full_name=org_name, inn=org_inn)
        return obj

    def create_update_entity(self, i):
        data_lst = RawData.objects.filter(num_proc=i).order_by('-pk')
        data = data_lst[0]
        data_hash = data.check_hash()
        try:
            entity = Procedures.objects.filter(proc_number=data.num_proc)[0]
        except:
            entity = Procedures()
        if (data_hash == entity.hash):
            return
        entity.places=Marketplaces.objects.get(full_name='portal_providers')
        entity.proc_number=data.num_proc
        entity.law=self.get_obj(Laws, data.law_proc)
        entity.type_proc=self.get_obj(TypesProc, data.type_proc)
        entity.orgs=self.get_org(data.partner) 
        entity.subject=data.subj_proc
        entity.date_start=pytz.timezone('Europe/Moscow').localize(datetime.strptime(data.start_date, '%d.%m.%Y'))
        entity.date_end=pytz.timezone('Europe/Moscow').localize(datetime.strptime(data.end_date, '%d.%m.%Y %H:%M'))
        entity.date_proc=pytz.timezone('Europe/Moscow').localize(datetime.strptime(data.end_date, '%d.%m.%Y %H:%M'))
        entity.tradeplace=Tradeplaces.objects.get(full_name='portal_providers')
        entity.stage=self.get_obj(Stages, data.status)
        entity.link=data.link_proc
        entity.deal_count=int(data.count_order) if data.count_order else 0
        entity.region=self.get_obj(Region, data.region)
        entity.hash=data_hash
        entity.save()
        print(i , 'complete')

    def get_rawdata(self, complete=False):
        if not self.rawdata:
            self.rawdata = RawData.objects.filter(complete=0)
        if not complete:
            return list(self.rawdata)
        else:
            self.rawdata.update(complete=1)
            del self.rawdata

    async def fillBase(self):
        start_time = time.time()
        get_rawdata_func = sync_to_async(self.get_rawdata, thread_sensitive=True)
        rawdata = await get_rawdata_func()
        lst = set([i.num_proc for i in rawdata])
        create_update_entity_async = sync_to_async(self.create_update_entity, thread_sensitive=False)
        for i in lst:
            await create_update_entity_async(i)
        await get_rawdata_func(True)
        print("--- %s seconds ---" % (time.time() - start_time))
        return len(lst)

class FullBase(ListView):
    template_name = 'indexpage/updatebase.html'
    model = Procedures
    paginate_by = 10
    queryset = Procedures.objects.order_by('-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inter_list = Interesting.objects.filter(user=self.user_id)
        if (len(inter_list)):
            context['inter_list'] = inter_list[0].procedure.all().values_list('proc_number', flat=True)
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        self.user_id = request.user.id
        return super().get(self, request, *args, **kwargs)

class InterestingBase(ListView):
    template_name = 'indexpage/updatebase.html'
    model = Procedures
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inter_list = Interesting.objects.filter(user=self.user_id)
        if (len(inter_list)):
            context['inter_list'] = inter_list[0].procedure.all().values_list('proc_number', flat=True)
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        print(request.user.id)
        try:
            self.queryset = Interesting.objects.get(user=request.user.id).procedure.all()
        except Exception as e:
            print(e)
            self.queryset = Interesting.objects.none()
        self.user_id = request.user.id
        return super().get(self, request, *args, **kwargs)


def add_Interesting(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not int(request.GET.get('value')):
        Interesting.objects.get(user=request.user.id).procedure.remove(Procedures.objects.get(pk=request.GET.get('pk')))
    else:
        inter = Interesting.objects.get(user=request.user.id)
        inter.procedure.add(*Procedures.objects.filter(pk=request.GET.get('pk')))
    return redirect(request.GET.get('next'))

# a4.publications.remove(p2)
# ['__and__', '__bool__', '__class__', '__class_getitem__', '__deepcopy__', '__delattr__', '__dict__', '__dir__', 
# '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', 
# '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__or__',
#  '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__',
#  '__weakref__', '_add_hints', '_annotate', '_batched_insert', '_chain', '_clone', '_combinator_query', '_db', '_defer_next_filter', 
# '_deferred_filter', '_earliest', '_extract_model_params', '_fetch_all', '_fields', '_filter_or_exclude', '_filter_or_exclude_inplace',
#  '_for_write', '_has_filters', '_hints', '_insert', '_iterable_class', '_iterator', '_known_related_objects', '_merge_known_related_objects',
#  '_merge_sanity_check', '_next_is_sticky', '_not_support_combined_queries', '_prefetch_done', '_prefetch_related_lookups',
#  '_prefetch_related_objects', '_prepare_for_bulk_create', '_query', '_raw_delete', '_result_cache', '_sticky_filter',
#  '_update', '_validate_values_are_expressions', '_values', 'aggregate', 'alias', 'all', 'annotate', 'as_manager', 
# 'bulk_create', 'bulk_update', 'complex_filter', 'contains', 'count', 'create', 'dates', 'datetimes', 'db', 'defer',
#  'delete', 'difference', 'distinct', 'earliest', 'exclude', 'exists', 'explain', 'extra', 'filter', 'first', 'get',
#  'get_or_create', 'in_bulk', 'intersection', 'iterator', 'last', 'latest', 'model', 'none', 'only', 'order_by', 
# 'ordered', 'prefetch_related', 'query', 'raw', 'resolve_expression', 'reverse', 'select_for_update', 'select_related', 
# 'union', 'update', 'update_or_create', 'using', 'values', 'values_list']

# <QuerySet [{'id': 364668, 'num_proc': '4123073', 'link_proc': 'https://zakupki.mos.ru/need/4123073', 'status': '?????????? ?????????????????????? ????????????????',
#  'type_proc': '?????????????? ???? ????????????????????????', 'partner': '?????????????????????????? ???????????????? ???????????????????? ???????????????????????? ???????????????? ?????????????? ?????????????????? (??????: 8901015840)',
#  'partner_inn': '8901015840', 'summ_proc': '599369', 'count_order': '1', 'region': '???? ??????????-????????????????', 'law_proc': '44-????', 'subj_proc': '?????????????? ???????????????????? ???? ???????????????? 2-?? ??????????????????',
#  'complete': 0, 'start_date': '09.07.2022', 'end_date': '09.07.2022 10:31', 'proc_comment': '???????????????????? ?? ??????'}]>