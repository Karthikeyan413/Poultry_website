#django forms 
from django import forms

class flt_form(forms.Form):
    bt_lyr_no = forms.IntegerField()
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
