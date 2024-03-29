from indexpage.models import Orgs, RawData, Procedures, Marketplaces,\
    Laws, TypesProc, Tradeplaces, Stages, Region
from usersProfile.models import ProfileUserModel
from .celery import app
from django.core.cache import cache
from datetime import datetime
import pytz
import time


class UpdateBase():
    def do(self):
        print('start')
        self.fillBase()
        print('end')

    def get_obj(self, model, value):
        try:
            obj = model.objects.get(full_name=value)
        except model.DoesNotExist:
            obj = model.objects.create(full_name=value)
        return obj

    def get_org(self, partner, partner_inn, update_name=False):
        org_inn = partner_inn
        org_name = partner
        try:
            obj: Orgs = Orgs.objects.get(inn=org_inn)
            if update_name and obj.full_name != org_name:
                obj.full_name = org_name
                obj.save()
        except Orgs.DoesNotExist:
            obj = Orgs.objects.create(full_name=org_name, inn=org_inn)
        return obj

    def create_update_entity(self, i):
        try:
            data_lst = RawData.objects.filter(num_proc=i[0]).order_by('-pk')
            data: RawData = data_lst[0]
            data_hash = data.check_hash()
            try:
                entity: Procedures = Procedures.objects.filter(
                    proc_number=data.num_proc)[0]
            except IndexError:
                entity = Procedures()
            if (data_hash == entity.hash):
                return
            entity.places = self.get_obj(Marketplaces, 'portal_providers')
            entity.proc_number = data.num_proc
            entity.law = self.get_obj(Laws, data.law_proc)
            entity.type_proc = self.get_obj(TypesProc, data.type_proc)
            entity.orgs = self.get_org(data.partner, data.partner_inn, True)
            entity.summ_proc = data.summ_proc
            entity.subject = data.subj_proc
            entity.date_start = pytz.timezone('Europe/Moscow').\
                localize(datetime.strptime(data.start_date, '%d.%m.%Y'))
            entity.date_end = pytz.timezone('Europe/Moscow').\
                localize(datetime.strptime(data.end_date, '%d.%m.%Y %H:%M'))
            entity.date_proc = pytz.timezone('Europe/Moscow').\
                localize(datetime.strptime(data.end_date, '%d.%m.%Y %H:%M'))
            entity.tradeplace = self.get_obj(Tradeplaces, 'portal_providers')
            entity.stage = self.get_obj(Stages, data.status)
            entity.link = data.link_proc
            entity.deal_count = int(data.count_order) if data.count_order else 0
            entity.region = self.get_obj(Region, data.region)
            entity.hash = data_hash
            entity.save()
            print(i[0] + ' complete')
        except ValueError as e:
            print(f'ERROR {e} {type(e)}')

    def fillBase(self):
        start_time = time.time()
        rawdata = RawData.objects.filter(complete=0).values_list('num_proc')
        print(len(set(rawdata)))
        set(map(self.create_update_entity, set(rawdata)))
        cache_base.delay()
        cache_old_base.delay()
        rawdata.update(complete=1)
        print("--- %s seconds ---" % (time.time() - start_time))
        return len(rawdata)


@app.task()
def cache_base():
    cache.set(
        'BASE', list(Procedures.objects.filter(
            date_proc__gte=datetime.today(),
            personal=False).order_by('-date_proc').values(
                'id', 'places__full_name', 'proc_number',
                'law__full_name', 'type_proc__full_name',
                'orgs__full_name', 'orgs__inn', 'subject',
                'date_start', 'date_end', 'date_proc',
                'tradeplace__full_name', 'stage__full_name',
                'link', 'created_at', 'deal_count',
                'region__full_name', 'summ_proc')), None)
    users_id = ProfileUserModel.objects.all().values('user')
    for user_id in users_id:
        cache_recomend.delay(user_id['user'])


@app.task()
def cache_old_base():
    cache.set('OLD_BASE', list(Procedures.objects.filter(
        personal=False).exclude(
            date_proc__gte=datetime.today()).order_by('-date_proc').values(
                'id', 'places__full_name', 'proc_number', 'law__full_name',
                'type_proc__full_name', 'orgs__full_name', 'orgs__inn',
                'subject', 'date_start', 'date_end', 'date_proc',
                'tradeplace__full_name', 'stage__full_name', 'link',
                'created_at', 'deal_count', 'region__full_name',
                'summ_proc')), None)


def find_element(elem: str, keys: str):
    if not keys.strip():
        return True
    for i in keys.replace(' ', '').lower().split(','):
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
                find_element(elem['type_proc__full_name'],
                             keywords['type_proc']) and
                find_element(elem['orgs__full_name'], keywords['orgs']) and
                find_element(elem['orgs__inn'], keywords['inn']) and
                find_element(elem['region__full_name'], keywords['region'])):
            recomend.append(elem)
    cache.set('RECOMEND' + str(user_id), recomend, None)
    return f'Cache user_id={user_id} complete'


@app.task()
def upd_base():
    UpdateBase().do()
