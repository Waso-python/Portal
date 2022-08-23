from django import forms
from .models import Procedures

class ProceduresForm(forms.ModelForm):
    places = forms.CharField(label='Место проведения', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    proc_number = forms.CharField(label='Номер процедуры', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    #law = forms.CharField(label='Закон', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    #type_proc = forms.CharField(label='Тип', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    orgs = forms.CharField(label='Организация', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    orgs_inn = forms.CharField(label='ИНН', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    subject = forms.CharField(label='Задача', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    date_start = forms.DateTimeField(label='Дата старта', widget=forms.SelectDateWidget(years=range(2020, 2031)), required=False)
    # time_start = forms.TimeField(label='Время старта')
    date_end = forms.DateTimeField(label='Дата рассмотрения', widget=forms.SelectDateWidget(years=range(2020, 2031)), required=False)
    # time_end = forms.TimeField(label='Время рассмотрения')
    date_proc = forms.DateTimeField(label='Прием заявок до', widget=forms.SelectDateWidget(years=range(2020, 2031)), required=False)
    # time_proc = forms.TimeField(label='Прием заявок до')
    tradeplace = forms.CharField(label='Торговая площадка', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    # stage = forms.CharField(label='Этап', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    link = forms.CharField(label='Ссылка', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    deal_count = forms.CharField(label='Кол-во заявок', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    # region = forms.CharField(label='Регион', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)

    class Meta:
        model = Procedures
        fields = ['law', 'type_proc', 'stage', 'region']
        pass