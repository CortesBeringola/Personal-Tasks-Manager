from django import forms

MONTH_CHOICES = [('JAN', 'JAN'), ('FEB', 'FEB'), ('MAR', 'MAR'), ('APR', 'APR'), ('MAY', 'MAY')]

class CreateNewExpense(forms.Form):

    name = forms.CharField(label="Name", max_length=200)
    amount = forms.FloatField()
    month = forms.CharField(widget=forms.Select(choices=MONTH_CHOICES))
    check = forms.BooleanField(required=False)
