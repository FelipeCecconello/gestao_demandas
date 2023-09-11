from django.contrib import admin
from .models import Curso, Aluno, Disciplina, Semestre, DisciplinasSemestre, AlunosPendentes, Professor, Turma, AlunosMatriculados

admin.site.register(Curso)
admin.site.register(Aluno)
admin.site.register(Disciplina)
admin.site.register(Semestre)
admin.site.register(DisciplinasSemestre)
admin.site.register(AlunosPendentes)
admin.site.register(Professor)
admin.site.register(Turma)
admin.site.register(AlunosMatriculados)