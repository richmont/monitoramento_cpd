from django import forms

class FormLoginGateway(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hostname_gateway'].widget.attrs.update({'class': 'form-control'})
        self.fields['porta_gateway'].widget.attrs.update({'class': 'form-control'})
        self.fields['login_gateway'].widget.attrs.update({'class': 'form-control'})
        self.fields['senha_gateway'].widget.attrs.update({'class': 'form-control'})

    
    hostname_gateway = forms.CharField(max_length=255)
    porta_gateway = forms.IntegerField(max_value=9999)
    login_gateway = forms.CharField(max_length=255)
    senha_gateway = forms.CharField(max_length=255, widget=forms.PasswordInput())
    