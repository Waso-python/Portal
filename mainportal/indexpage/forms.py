from django import forms


class UserOrgsForm(forms.Form):
    my_org = forms.ModelChoiceField(label='Организации', queryset=None, widget=forms.Select(attrs={'class': 'form-control', 'cols': 10}))


class UserOrdersForm(forms.Form):
    amount = forms.CharField(label='Сумма', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    comment = forms.CharField(label='Коментарий', max_length=1000, widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}), required=False)
    win = forms.BooleanField(label='Победили', required=False)


class UserContractsForm(forms.Form):
    contract_num = forms.CharField(label='Сумма', max_length=255, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    contract_date = forms.DateField(label='Дата контракта', widget=forms.SelectDateWidget(years=range(2015,2031)), required=False)
    deadline = forms.DateField(label='Крайний срок поставки', widget=forms.SelectDateWidget(years=range(2015,2031)), required=False)
    day_to_shipping = forms.IntegerField(label='Дней на поставку', required=False)
    comment = forms.CharField(label='Коментарий', max_length=1000, widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}), required=False)


class ProceduresForm(forms.Form):
    places = forms.CharField(label='Место проведения', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    proc_number = forms.CharField(label='Номер процедуры', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    law = forms.CharField(label='Закон', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    type_proc = forms.CharField(label='Тип', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    orgs = forms.CharField(label='Организация', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    subject = forms.CharField(label='Задача', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    date_start = forms.DateTimeField(label='Дата старта', widget=forms.SelectDateWidget(years=range(2020, 2031)), required=False)
    # time_start = forms.TimeField(label='Время старта')
    date_end = forms.DateTimeField(label='Дата рассмотрения', widget=forms.SelectDateWidget(years=range(2020, 2031)), required=False)
    # time_end = forms.TimeField(label='Время рассмотрения')
    date_proc = forms.DateTimeField(label='Прием заявок до', widget=forms.SelectDateWidget(years=range(2020, 2031)), required=False)
    # time_proc =  forms.TimeField(label='Прием заявок до')
    tradeplace = forms.CharField(label='Торговая площадка', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    stage = forms.CharField(label='Этап', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    link = forms.CharField(label='Ссылка', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    summ_proc = forms.CharField(label='Сумма', max_length=20, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    deal_count = forms.CharField(label='Кол-во заявок', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    region = forms.CharField(label='Регион', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
