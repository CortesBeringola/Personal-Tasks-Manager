from django import forms

MONTH_CHOICES = [('Jan','Jan'), ('Feb', 'Feb'), ('Mar', 'Mar'), ('Apr', 'Apr'), ('May', 'May'), ('Jun', 'Jun'),
                 ('Jul', 'Jul'),('Aug', 'Aug'), ('Sep', 'Sep'), ('Oct', 'Oct'), ('Nov', 'Nov'), ('Dec', 'Dec')]

class CreateNewExpense(forms.Form):

    name = forms.CharField(label="Name", max_length=200)
    amount = forms.FloatField()
    month = forms.CharField(widget=forms.Select(choices=MONTH_CHOICES))
    check = forms.BooleanField(required=False)
