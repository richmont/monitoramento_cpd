from django import forms
from monitoramento_cpd_app.models.impressoras import Impressora


class ImpressoraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class': 'form-control'})
        self.fields['IP'].widget.attrs.update({'class': 'form-control'})
        self.fields['local'].widget.attrs.update({'class': 'form-control'})
        self.fields['modelo'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Impressora
        fields = ["nome", "local", "IP", "modelo"]
