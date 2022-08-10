from django import forms
from indexpage.models import Laws

class KeysForm(forms.Form):
    places = forms.CharField(label='Сайт', max_length=255, widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}), required=False)
    law = forms.CharField(label='Закон', max_length=255, widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}), required=False)
    type_proc = forms.CharField(label='Тип', max_length=255, widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}), required=False)
    orgs = forms.CharField(label='Организация', max_length=255, widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}), required=False)
    inn = forms.CharField(label='ИНН', max_length=255, widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}), required=False)
    subject = forms.CharField(label='Задача', max_length=255, widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}), required=False)
    region = forms.CharField(label='Регион', max_length=255, widget=forms.Textarea(attrs={'cols': 50, 'rows': 3}), required=False)

class LawForm(forms.ModelForm):
    class Meta():
        model = Laws
        fields = ['full_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update({"class": "form-control"})
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':"form-control"})