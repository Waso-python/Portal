from django import forms

class UserOrdersForm(forms.Form):
    my_org = forms.ModelChoiceField(label='Организации', queryset=None, widget=forms.Select(attrs={'class': 'form-control', 'cols': 10}))
    amount = forms.CharField(label='Сумма', max_length=250, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}), required=False)
    comment = forms.CharField(label='Коментарий', max_length=1000, widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}), required=False)
    win = forms.BooleanField(label='Победили', required=False)


# org = forms.ModelChoiceField(queryset=Org.objects.all(),  widget=forms.Select(attrs={'class': 'form-control'}), required=True)