from django import forms
from monitoramento_cpd_app.models.pdvs import PDV


class FormPDV(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['IP'].widget.attrs.update({'class': 'form-control'})
        self.fields['checkout'].widget.attrs.update({'class': 'form-control'})
        self.fields['tipo_pdv'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = PDV
        fields = ["IP", "checkout", "tipo_pdv"]