"""
URL configuration for gestao_demandas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gestao.views import *
from relatorios.views import relatorio_semestre, lista_relatorios, lista_relatorios_disciplinas, gerar_relatorio_disciplina
app_name = 'relatorios'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('curso/<str:curso_codigo>/semestres/criar/', CriarSemestreView.as_view(), name='criar_semestre'),
    path('curso/<str:curso_codigo>/semestres/', ListaSemestresView.as_view(), name='lista_semestres'),
    path('curso/<str:curso_codigo>/semestres/<str:semestre_codigo>/preencher_disciplinas/', PreencherDisciplinasSemestreView.as_view(), name='preencher_disciplinas'),
    path('curso/listar/', ListaCursosView.as_view(), name='lista_cursos'),
    path('curso/<str:curso_codigo>/', DetalhesCursoView.as_view(), name='detalhes_curso'),
    path('curso/<str:curso_codigo>/inserir_alunos/', InserirAlunosCursoView.as_view(), name='inserir_alunos_curso'),
    path('curso/<str:curso_codigo>/inserir_disciplinas/', InserirDisciplinasCursoView.as_view(), name='inserir_disciplinas_curso'),
    path('curso/<str:curso_codigo>/inserir_professores/', InserirProfessoresCursoView.as_view(), name='inserir_professores_curso'),
    path('curso/<str:curso_codigo>/semestres/<str:semestre_codigo>/preencher_alunos_pendentes/', PreencherAlunosPendentesView.as_view(), name='preencher_alunos_pendentes'),
    path('curso/<str:curso_codigo>/semestres/<str:semestre_codigo>/preencher_turmas/', PreencherTurmasView.as_view(), name='preencher_turmas'),
    path('curso/<int:curso_codigo>/semestres/<int:semestre_codigo>/escolher_professores/', EscolherProfessoresView.as_view(), name='escolher_professores'),
    path('curso/<str:curso_codigo>/semestres/<str:semestre_codigo>/preencher_alunos_matriculados/', PreencherAlunosMatriculadosView.as_view(), name='preencher_alunos_matriculados'),
    path('relatorios/<int:semestre_id>/relatorio_geral/', relatorio_semestre, name='relatorio_semestre'),
    path('relatorios/', lista_relatorios, name='lista_semestres'),
    path('relatorios/<int:semestre_id>/', lista_relatorios_disciplinas, name='lista_relatorios_disciplinas'),
    path('relatorios/<int:semestre_id>/<int:disciplina_semestre_codigo>/', gerar_relatorio_disciplina, name='gerar_relatorio_disciplina'),
]
