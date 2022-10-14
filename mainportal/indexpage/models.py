from django.db import models
from django.contrib.auth.models import User
from indexpage.forms import UserOrdersForm, UserContractsForm
import datetime
import hashlib


class Order(models.Model):
    ACTUAL_ANSWER = (
        (0, 'не актуально'),
        (1, 'актуально')
    )
    num_proc = models.CharField(max_length=10, null=False)
    link_proc = models.CharField(max_length=500, null=False)
    partner = models.CharField(max_length=512, null=False)
    summ_proc = models.IntegerField(null=False)
    count_order = models.IntegerField(null=False)

    subj_proc = models.CharField(max_length=512)
    actual_for_me = models.IntegerField(choices = ACTUAL_ANSWER)
    end_date = models.DateTimeField()
    add_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.subj_proc} until {self.end_date}'

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        'DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class PortalGroups(models.Model):
    name = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'portal_groups'

class RawData(models.Model):
    num_proc = models.CharField(max_length=128)
    link_proc = models.CharField(max_length=500)
    status = models.CharField(max_length=128)
    type_proc = models.CharField(max_length=128)
    partner = models.CharField(max_length=512)
    partner_inn = models.CharField(max_length=512)
    summ_proc = models.CharField(max_length=20)
    count_order = models.CharField(max_length=5)
    region = models.CharField(max_length=128)
    law_proc = models.CharField(max_length=128)
    subj_proc = models.CharField(max_length=512)
    complete = models.IntegerField(default=0)
    start_date = models.CharField(max_length=50)
    end_date = models.CharField(max_length=50)
    proc_comment = models.CharField(max_length=256)
    inserted_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self) -> str:
        return f'{self.id} - {self.num_proc} - {self.complete}'

    def check_hash(self):
        return hashlib.sha224((self.link_proc + self.status + self.type_proc + self.partner 
                    + self.partner_inn + self.summ_proc + self.count_order + self.region 
                    + self.law_proc + self.subj_proc + self.start_date + self.end_date 
                    + self.proc_comment).encode('utf-8') ).hexdigest()

    class Meta:
        managed = True
        db_table = 'raw_table'


class IndexpageOrder(models.Model):
    id = models.BigAutoField(primary_key=True)
    num_proc = models.CharField(max_length=10)
    link_proc = models.CharField(max_length=500)
    partner = models.CharField(max_length=512)
    summ_proc = models.IntegerField()
    count_order = models.IntegerField()
    subj_proc = models.CharField(max_length=512)
    actual_for_me = models.IntegerField()
    add_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'indexpage_order'


class Laws(models.Model):
    full_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'{self.id} - {self.full_name}'

    class Meta:
        managed = True
        db_table = 'laws'


class Marketplaces(models.Model):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.id} - {self.full_name}'

    class Meta:
       db_table = 'marketplaces'


class Orgs(models.Model):
    full_name = models.CharField(max_length=512, blank=True, null=True)
    short_name = models.CharField(max_length=512, blank=True, null=True)
    email = models.CharField(max_length=512, blank=True, null=True)
    phone = models.CharField(max_length=512, blank=True, null=True)
    url = models.CharField(max_length=512, blank=True, null=True)
    inn = models.CharField(max_length=512, blank=True, null=True)
    cod_reestr = models.CharField(max_length=512, blank=True, null=True)
    date_reg = models.DateTimeField(blank=True, null=True)
    date_last_change = models.DateTimeField(blank=True, null=True)
    kpp = models.CharField(max_length=512, blank=True, null=True)
    ogrn = models.CharField(max_length=512, blank=True, null=True)
    oktmo = models.CharField(max_length=512, blank=True, null=True)
    iku = models.CharField(max_length=512, blank=True, null=True)
    date_iku = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.id} - {self.full_name}'

    class Meta:
        db_table = 'orgs'


class Peoples(models.Model):
    full_name = models.CharField(max_length=512, blank=True, null=True)
    surname = models.CharField(max_length=512, blank=True, null=True)
    name = models.CharField(max_length=512, blank=True, null=True)
    name2 = models.CharField(max_length=512, blank=True, null=True)
    email = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    org = models.ForeignKey(Orgs, models.DO_NOTHING, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.id} - {self.full_name}'

    class Meta:
        db_table = 'peoples'

class Region(models.Model):
    full_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'{self.id} - {self.full_name}'

    def __unicode__(self):
        return u'%s' % self.full_name

class Procedures(models.Model):
    places = models.ForeignKey(Marketplaces, models.DO_NOTHING, blank=True, null=True)
    proc_number = models.CharField(max_length=512)
    law = models.ForeignKey(Laws, models.DO_NOTHING, db_column='law')
    type_proc = models.ForeignKey('TypesProc', models.DO_NOTHING, db_column='type_proc')
    orgs = models.ForeignKey(Orgs, models.DO_NOTHING, blank=True, null=True)
    subject = models.CharField(max_length=512, blank=True, null=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)
    date_proc = models.DateTimeField(blank=True, null=True)
    tradeplace = models.ForeignKey('Tradeplaces', models.DO_NOTHING, db_column='tradeplace')
    stage = models.ForeignKey('Stages', models.DO_NOTHING, db_column='stage')
    link =  models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    deal_count = models.IntegerField()
    region = models.ForeignKey('Region', models.DO_NOTHING, blank=True, null=True)
    summ_proc = models.CharField(max_length=20, blank=True, null=True)
    hash = models.CharField(max_length=200, null=True)
    personal = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.id} - {self.proc_number} - {self.subject}'

    def get_form_dict(self):
        return {
            'places': self.places.full_name,
            'proc_number': self.personal_proc_num(),
            'law': self.law,
            'type_proc': self.type_proc, 
            'orgs': self.orgs.full_name,
            'orgs_inn': self.orgs.inn,
            'subject': self.subject, 
            'date_start': self.date_start,
            'hours_start': self.date_start.hour if self.date_start is not None else 0,
            'minutes_start': self.date_start.minute if self.date_start is not None else 0,
            'date_end': self.date_end,
            'hours_end': self.date_end.hour if self.date_end is not None else 0,
            'minutes_end': self.date_end.minute if self.date_end is not None else 0,
            'date_proc': self.date_proc,
            'hours_proc': self.date_proc.hour if self.date_proc is not None else 0,
            'minutes_proc': self.date_proc.minute if self.date_proc is not None else 0,
            'summ_proc': self.summ_proc,
            'tradeplace': self.tradeplace.full_name, 
            'stage': self.stage,
            'link': self.link,
            'deal_count': self.deal_count,
            'region': self.region}

    def personal_proc_num(self):
        return self.proc_number.split('<-!->')[0]

    class Meta:
        db_table = 'procedures'


class Stages(models.Model):
    full_name = models.CharField(max_length=512)

    def __str__(self) -> str:
        return f'{self.id} - {self.full_name}'

    class Meta:
        db_table = 'stages'


class Tradeplaces(models.Model):
    full_name = models.CharField(max_length=512, null=True, blank=True)
    link = models.CharField(max_length=521, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.id} - {self.full_name}'

    class Meta:
        db_table = 'tradeplaces'


class TypesProc(models.Model):
    full_name = models.CharField(max_length=512)

    def __str__(self) -> str:
        return f'{self.id} - {self.full_name}'

    class Meta:
        db_table = 'types_proc'


class PortalUsers(models.Model):
    full_name = models.CharField(max_length=512, blank=True, null=True)
    password = models.CharField(max_length=512, blank=True, null=True)
    email = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    group = models.ForeignKey(PortalGroups, models.DO_NOTHING, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.id} - {self.full_name}'

    class Meta:
        db_table = 'portal_users'

class Interesting(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    procedure = models.ManyToManyField(Procedures)

class UserOrders(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    procedure = models.ForeignKey(Procedures, models.DO_NOTHING)
    my_org = models.ForeignKey('UserOrgs', models.CASCADE)
    amount = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=1024, blank=True, null=True)
    win = models.BooleanField(blank=True, null=True)

    def get_orders_form(self):
        return UserOrdersForm(initial={'amount':self.amount,
                                       'comment':self.comment,
                                       'win':self.win})

    def get_contracts_form(self):
        contract = UserContracts.objects.get(order=self)
        return UserContractsForm(initial={
            'contract_num': contract.contract_num,
            'contract_date': contract.contract_date,
            'deadline': contract.deadline,
            'day_to_shipping': contract.day_to_shipping,
            'comment': contract.comment})

    def __str__(self):
        return f'{self.my_org}'

class UserOrgs(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

class UserContracts(models.Model):
    order = models.ForeignKey(UserOrders, models.CASCADE)
    contract_num = models.CharField(max_length=255, blank=True, null=True)
    contract_date = models.DateField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    day_to_shipping = models.SmallIntegerField(blank=True, null=True)
    comment = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f'{self.order.procedure}  {self.deadline}'