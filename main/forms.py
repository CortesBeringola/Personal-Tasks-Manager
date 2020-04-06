from django import forms
from .models import ToDoList

class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=300, widget=forms.Textarea)
    check = forms.BooleanField(required=False)

    class Meta:
        model = ToDoList

    def __init__(self, *args, **kwargs):
        super(CreateNewList, self).__init__(*args, **kwargs)  # Call to ModelForm constructor
        self.fields['name'].widget.attrs['style'] = 'width:80%; height:60px;'

