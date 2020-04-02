from django import forms

class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=200,widget=forms.TextInput(attrs={'class':'special', 'width':'100'}))
    check = forms.BooleanField(required=False)
