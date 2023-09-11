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

class AlunosMatriculadosForm(forms.Form):
    matriculas = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), required=False)
    
class CriarSemestreForm(forms.ModelForm):
    class Meta:
        model = Semestre
        fields = ['numero']

class PreencherTurmasForm(forms.Form):
    def __init__(self, *args, **kwargs):
        disciplinas_semestre = kwargs.pop('disciplinas_semestre', None)  # Remova o argumento do construtor
        super(PreencherTurmasForm, self).__init__(*args, **kwargs)

        if disciplinas_semestre is not None:
            for disciplina_semestre in disciplinas_semestre:
                self.fields[f'num_turmas_{disciplina_semestre.pk}'] = forms.IntegerField(
                    label=f'Número de Turmas para {disciplina_semestre.disciplina.nome}',
                    min_value=1,  # Define o valor mínimo como 1
                    initial=1,    # Define o valor inicial como 1
                    required=True,
                    widget=forms.NumberInput(attrs={'class': 'form-control'}),
                )
