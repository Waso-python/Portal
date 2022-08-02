from indexpage.models import *
from datetime import datetime
import pytz
import time
from .celery import app

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
        data_lst = RawData.objects.filter(num_proc=i).order_by('-pk')
        data = data_lst[0]
        data_hash = data.check_hash()
        try:
            entity = Procedures.objects.filter(proc_number=data.num_proc)[0]
        except:
            entity = Procedures()
        if (data_hash == entity.hash):
            print(i, 'old')
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


    def fillBase(self):
        start_time = time.time()
        rawdata =  RawData.objects.filter(complete=0)
        lst = set([i.num_proc for i in rawdata])
        for i in lst:
            self.create_update_entity(i)
        rawdata.update(complete=1)
        print("--- %s seconds ---" % (time.time() - start_time))
        return len(lst)

@app.task()
def upd_base():
    UpdateBase().do()