from django.contrib import admin
from .models import Curso, Aluno, Disciplina, Semestre, DisciplinasSemestre, AlunosPendentes

admin.site.register(Curso)
admin.site.register(Aluno)
admin.site.register(Disciplina)
admin.site.register(Semestre)
admin.site.register(DisciplinasSemestre)
admin.site.register(AlunosPendentes)