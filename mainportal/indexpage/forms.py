from django import forms
from .models import UserOrders

class UserOrdersForm(forms.ModelForm):
    class Meta:
        model = UserOrders
        my_org = forms.ModelChoiceField(queryset=None)
        fields = ['my_org', 'amount', 'comment', 'win']
        widgets = {
            'amount': forms.Textarea(attrs={'cols': 30, 'rows': 1}),
            'comment': forms.Textarea(attrs={'cols': 50, 'rows':2}),
        }
        labels = {
            'my_org':'Организация',
            'amount':'Сумма',
            'comment':'Коментарий',
            'win':'Победа',
        } 

# org = forms.ModelChoiceField(queryset=Org.objects.all(),  widget=forms.Select(attrs={'class': 'form-control'}), required=True)