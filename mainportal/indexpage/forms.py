from django import forms

class UserOrgsForm(forms.Form):
    my_org = forms.ModelChoiceField(label='Организации', queryset=None, widget=forms.Select(attrs={'class': 'form-control', 'cols': 10}))

class UserOrdersForm(forms.Form):
    amount = forms.CharField(label='Сумма', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    comment = forms.CharField(label='Коментарий', max_length=1000, widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}), required=False)
    win = forms.BooleanField(label='Победили', required=False)

class UserContractsForm(forms.Form):
    contract_num = forms.CharField(label='Сумма', max_length=255, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    contract_date = forms.DateField(label='Дата контракта' ,required=False)
    deadline = forms.DateField(label='Крайний срок поставки', required=False)
    day_to_shipping = forms.IntegerField(label='Дней на поставку', required=False)
    comment = forms.CharField(label='Коментарий', max_length=1000, widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}), required=False)