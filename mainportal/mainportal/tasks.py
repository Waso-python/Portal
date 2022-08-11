from ast import keyword
from indexpage.models import *
from usersProfile.models import ProfileUserModel
from datetime import datetime
import pytz
import time
from .celery import app
from django.core.cache import cache
from datetime import datetime

class UpdateBase():
    def do(self):
        print('start')
        self.fillBase()
        print('end')

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
        data_lst = RawData.objects.filter(num_proc=i[0]).order_by('-pk')
        data = data_lst[0]
        data_hash = data.check_hash()
        try:
            entity = Procedures.objects.filter(proc_number=data.num_proc)[0]
        except IndexError:
            entity = Procedures()
        # if (data_hash == entity.hash):
        #     return
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
        print(i[0] + ' complete')

    def fillBase(self):
        start_time = time.time()
        rawdata =  RawData.objects.filter(complete=0).values_list('num_proc')
        print(len(set(rawdata)))
        set(map(self.create_update_entity, set(rawdata)))
        if len(rawdata) > 0:
            cache_base.delay()
            cache_old_base.delay()
            rawdata.update(complete=1)
        print("--- %s seconds ---" % (time.time() - start_time))
        return len(rawdata)

@app.task()
def cache_base():
    cache.set('BASE', list(Procedures.objects.filter(date_proc__gte = datetime.today()).order_by('-date_proc').values('id', 'places__full_name', 'proc_number', 'law__full_name', 
                    'type_proc__full_name', 'orgs__full_name', 'orgs__inn', 'subject', 'date_start', 'date_end', 'date_proc', 'tradeplace__full_name', 
                    'stage__full_name', 'link', 'created_at', 'deal_count', 'region__full_name')), None)
    users_id = ProfileUserModel.objects.all().values('user')
    for user_id in users_id:
        cache_recomend.delay(user_id['user'])

@app.task()
def cache_old_base():
    cache.set('OLD_BASE', list(Procedures.objects.exclude(date_proc__gte = datetime.today()).order_by('-date_proc').values('id', 'places__full_name', 'proc_number', 
                    'law__full_name', 'type_proc__full_name', 'orgs__full_name', 'orgs__inn', 'subject', 'date_start', 'date_end', 'date_proc', 'tradeplace__full_name', 
                    'stage__full_name', 'link', 'created_at', 'deal_count', 'region__full_name')), None)

def find_element(elem: str, keys: str):
    if not keys.strip():
        return True
    for i in keys.replace(' ','').lower().split(','):
        if i and i in elem.lower():
            return True
    return False

@app.task()
def cache_recomend(user_id):
    recomend = []
    base = cache.get('BASE')
    keywords = ProfileUserModel.objects.get(user=user_id).keys
    print(keywords)
    for elem in base:
        if (find_element(elem['subject'], keywords['subject']) and
            find_element(elem['places__full_name'], keywords['places']) and
            find_element(elem['law__full_name'], keywords['law']) and
            find_element(elem['type_proc__full_name'], keywords['type_proc']) and
            find_element(elem['orgs__full_name'], keywords['orgs']) and
            find_element(elem['orgs__inn'], keywords['inn']) and
            find_element(elem['region__full_name'], keywords['region'])):
            recomend.append(elem)
    cache.set('RECOMEND' +  str(user_id), recomend, None)
    return f'Cache user_id={user_id} complete'


@app.task()
def upd_base():
    UpdateBase().do()


# ('компьютер', 'принтер', 'заправка', 'картридж', 'подароч', 'комплектующ', 'ноутбук')