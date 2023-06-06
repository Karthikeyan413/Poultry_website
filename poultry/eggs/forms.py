#django forms 
from django import forms

class flt_form(forms.Form):
    bt_no = forms.IntegerField()
    lyr_no = forms.IntegerField()
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

class add_form(forms.Form):
    roles = [('A','admin'),
             ('S','supervisor'),
             ('O','office_staff')]
    username = forms.CharField()
    pwd = forms.CharField(widget=forms.TextInput(attrs={'type': 'password'}))
    role = forms.ChoiceField(choices=roles)