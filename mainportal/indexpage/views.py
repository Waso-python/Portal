from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView, ListView
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
    paginate_by = 10
    queryset = cache.get('BASE')

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
        print(len(request.GET))
        print(str(request.user.id) + 'inter' + str(request.GET['page'] if len(request.GET) != 0 else '1'))
        page = cache.get(str(request.user.id) + 'inter' + str(request.GET['page'] if len(request.GET) != 0 else '1'))
        if page:
            return page
        if not request.user.is_authenticated:
            return redirect('login')
        try:
            self.queryset = Interesting.objects.get(user=request.user.id).procedure.all()
        except Exception as e:
            print(e)
            self.queryset = Interesting.objects.none()
        self.user_id = request.user.id
        page = super().get(self, request, *args, **kwargs).render()
        cache.set(str(request.GET['page'] if len(request.GET) != 0 else '1'), page)
        return page


def add_Interesting(request):
    if not request.user.is_authenticated:
        return redirect('login')
    print(request.GET)
    if not int(request.GET.get('value')):
        Interesting.objects.get(user=request.user.id).procedure.remove(Procedures.objects.get(pk=request.GET.get('pk')))
        cache.set('WTF', None)
    else:
        inter = Interesting.objects.get(user=request.user.id)
        inter.procedure.add(*Procedures.objects.filter(pk=request.GET.get('pk')))
        cache.set(str('fghm' if len(request.GET) != 0 else '1'), None)
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
 
# <QuerySet [{'id': 364668, 'num_proc': '4123073', 'link_proc': 'https://zakupki.mos.ru/need/4123073', 'status': 'Прием предложений завершен',
#  'type_proc': 'Закупка по потребностям', 'partner': 'МУНИЦИПАЛЬНОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ САЛЕХАРДСКАЯ ДИРЕКЦИЯ ЕДИНОГО ЗАКАЗЧИКА (ИНН: 8901015840)',
#  'partner_inn': '8901015840', 'summ_proc': '599369', 'count_order': '1', 'region': 'АО Ямало-Ненецкий', 'law_proc': '44-ФЗ', 'subj_proc': 'Засыпка котлованов на кладбище 2-е отделение',
#  'complete': 0, 'start_date': '09.07.2022', 'end_date': '09.07.2022 10:31', 'proc_comment': 'Интеграция с РИС'}]>