from django import forms
from django.forms import ModelForm, ModelMultipleChoiceField, SelectMultiple

from .models import *

class PreencherDisciplinasSemestreForm(forms.Form):
    disciplinas = forms.ModelMultipleChoiceField(
        queryset=Disciplina.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False  # Permite que nenhuma disciplina seja selecionada inicialmente
    )

class AlunosPendentesForm(forms.Form):
    matriculas = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), required=False)
    
class CriarSemestreForm(forms.ModelForm):
    class Meta:
        model = Semestre
        fields = ['numero']