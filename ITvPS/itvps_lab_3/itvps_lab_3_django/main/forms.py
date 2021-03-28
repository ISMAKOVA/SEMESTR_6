from django import forms


class MyForm(forms.Form):
    file = forms.CharField(required=False, label=False)
    file.widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Название файла',
            'aria-label': 'file',
            'aria-describedby': 'btn',

        })

