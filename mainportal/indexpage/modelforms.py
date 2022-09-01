from django import forms
from .models import Procedures

FRUIT_CHOICES= [
    ('orange', 'Oranges'),
    ('cantaloupe', 'Cantaloupes'),
    ('mango', 'Mangoes'),
    ('honeydew', 'Honeydews'),
    ]

class ProceduresForm(forms.ModelForm):
    places = forms.CharField(label='Место проведения', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    proc_number = forms.CharField(label='Номер процедуры', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    orgs = forms.CharField(label='Организация', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    orgs_inn = forms.CharField(label='ИНН', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    subject = forms.CharField(label='Задача', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    date_start = forms.DateTimeField(label='Дата старта', widget=forms.SelectDateWidget(years=range(2020, 2031)))
    hours_start = forms.CharField(label='часы', widget=forms.Select(choices=((i,i) for i in range(24))))
    minutes_start = forms.CharField(label='минуты', widget=forms.Select(choices=((i,i) for i in range(0, 51, 10))))
    date_end = forms.DateTimeField(label='Дата рассмотрения', widget=forms.SelectDateWidget(years=range(2020, 2031)))
    hours_end = forms.CharField(label='часы', widget=forms.Select(choices=((i,i) for i in range(24))))
    minutes_end = forms.CharField(label='минуты', widget=forms.Select(choices=((i,i) for i in range(0, 51, 10))))
    date_proc = forms.DateTimeField(label='Прием заявок до', widget=forms.SelectDateWidget(years=range(2020, 2031)))
    hours_proc = forms.CharField(label='часы', widget=forms.Select(choices=((i,i) for i in range(24))))
    minutes_proc = forms.CharField(label='минуты', widget=forms.Select(choices=((i,i) for i in range(0, 51, 10))))
    tradeplace = forms.CharField(label='Торговая площадка', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    link = forms.CharField(label='Ссылка', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    deal_count = forms.CharField(label='Кол-во заявок', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    summ_proc = forms.CharField(label='Сумма', max_length=20, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)


    class Meta:
        model = Procedures
        fields = ['law', 'type_proc', 'stage', 'region']
        labels = {'law': 'Закон','type_proc': 'Тип',
                  'stage': 'Этап', 'region': 'Регион'}
        widgets = {'law': forms.Select(attrs={'class': 'form-control', 'cols': 10}),
                   'type_proc': forms.Select(attrs={'class': 'form-control', 'cols': 10}),
                   'stage': forms.Select(attrs={'class': 'form-control', 'cols': 10}),
                   'region': forms.Select(attrs={'class': 'form-control', 'cols': 10})}