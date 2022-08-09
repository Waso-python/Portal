from django import forms

class KeysForm(forms.Form):
    places = forms.CharField(label='Сайт', max_length=255, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}))
    law = forms.CharField(label='Закон', max_length=255, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}))
    type_proc = forms.CharField(label='Тип', max_length=255, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}))
    orgs = forms.CharField(label='Организация', max_length=255, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}))
    subject = forms.CharField(label='Задача', max_length=255, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}))
    region = forms.CharField(label='Регион', max_length=255, widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}))

    def save_keys(self):
        print(self.places)
        pass