from django import forms
from monitoramento_cpd_app.models.workstations import Workstation


class WorkstationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hostname'].widget.attrs.update({'class': 'form-control'})
        self.fields['IP'].widget.attrs.update({'class': 'form-control'})
        self.fields['dominio'].widget.attrs.update({'class': 'form-control'})
        self.fields['local'].widget.attrs.update({'class': 'form-control'})
        self.fields['modelo'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Workstation
        fields = ["hostname", "IP", "dominio", "local", "modelo"]
