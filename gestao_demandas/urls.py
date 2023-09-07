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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('curso/<str:curso_codigo>/semestres/criar/', CriarSemestreView.as_view(), name='criar_semestre'),
    path('curso/<str:curso_codigo>/semestres/', ListaSemestresView.as_view(), name='lista_semestres'),
    path('curso/<str:curso_codigo>/semestres/<str:semestre_codigo>/preencher_disciplinas/', PreencherDisciplinasSemestreView.as_view(), name='preencher_disciplinas'),
    path('curso/listar/', ListaCursosView.as_view(), name='lista_cursos'),
    path('curso/<str:curso_codigo>/', DetalhesCursoView.as_view(), name='detalhes_curso'),
    path('curso/<str:curso_codigo>/inserir_alunos/', InserirAlunosCursoView.as_view(), name='inserir_alunos_curso'),
    path('curso/<str:curso_codigo>/semestres/<str:semestre_codigo>/preencher_alunos_pendentes/', PreencherAlunosPendentesView.as_view(), name='preencher_alunos_pendentes'),
]