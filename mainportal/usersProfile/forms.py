from django import forms

class KeysForm(forms.Form):
    places = forms.CharField(label='Сайт', max_length=255, widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}), required=False)
    law = forms.CharField(label='Закон', max_length=255, widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}), required=False)
    type_proc = forms.CharField(label='Тип', max_length=255, widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}), required=False)
    orgs = forms.CharField(label='Организация', max_length=255, widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}), required=False)
    inn = forms.CharField(label='ИНН', max_length=255, widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}), required=False)
    subject = forms.CharField(label='Задача', max_length=255, widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}), required=False)
    region = forms.CharField(label='Регион', max_length=255, widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}), required=False)