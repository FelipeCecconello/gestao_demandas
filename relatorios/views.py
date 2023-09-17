# No arquivo views.py do seu app relatorios
from django.shortcuts import render, get_object_or_404
from gestao.models import Semestre, Curso, DisciplinasSemestre, AlunosPendentes, AlunosMatriculados
from .relatorios import gerar_relatorio

def relatorio_semestre(request, semestre_id):
    semestre = Semestre.objects.get(pk=semestre_id)
    df = gerar_relatorio(semestre_id)

    # Converter o DataFrame em HTML para renderização no template
    relatorio_html = df.to_html(classes='table table-bordered table-striped')

    context = {
        'semestre': semestre,
        'relatorio_html': relatorio_html,
    }

    return render(request, 'relatorio_semestre.html', context)

def lista_relatorios(request):
    # Filtrar os semestres do curso de SI
    curso = Curso.objects.get(pk=1)
    semestres_si = Semestre.objects.filter(curso=curso)

    return render(request, 'lista_relatorios.html', {'semestres_si': semestres_si})

def lista_relatorios_disciplinas(request, semestre_id):
    semestre = Semestre.objects.get(pk=semestre_id)
    disciplinas_semestre = DisciplinasSemestre.objects.filter(semestre=semestre)

    context = {
        'disciplinas_semestre': disciplinas_semestre,
        'semestre_id': semestre_id,
    }

    return render(request, 'lista_relatorios_disciplinas.html', context)

def gerar_relatorio_disciplina(request, semestre_id, disciplina_semestre_codigo):
    disciplina_semestre = get_object_or_404(DisciplinasSemestre, pk=disciplina_semestre_codigo)
    
    # Filtrar os alunos pendentes e matriculados para a disciplina
    alunos_pendentes = AlunosPendentes.objects.filter(disciplina_semestre=disciplina_semestre, aluno__curso__codigo=1)
    alunos_matriculados = AlunosMatriculados.objects.filter(turma__disciplina_semestre=disciplina_semestre, aluno__curso__codigo=1)
    
    # Criar um conjunto (set) de alunos únicos
    alunos_unicos = set()
    
    for aluno_pendente in alunos_pendentes:
        alunos_unicos.add(aluno_pendente.aluno)

    for aluno_matriculado in alunos_matriculados:
        alunos_unicos.add(aluno_matriculado.aluno)

    # Criar uma lista de alunos com as informações necessárias para o relatório
    relatorio_data = []

    for aluno in alunos_unicos:
        esta_matriculado = AlunosMatriculados.objects.filter(aluno=aluno, turma__disciplina_semestre=disciplina_semestre).exists()
        situacao_geral = 'REGULAR' if esta_matriculado else 'IRREGULAR'
        relatorio_data.append({'matricula': aluno.matricula, 'nome': aluno.nome, 'situacao': 'MATRICULADO' if esta_matriculado else 'PENDENTE', 'situacao_geral': situacao_geral})

    return render(request, 'relatorio_disciplina.html', {'semestre_id': semestre_id, 'disciplina_semestre': disciplina_semestre, 'relatorio_data': relatorio_data})

def aluno_esta_regular(aluno, semestre_id):
    # Verifique se o aluno está matriculado em qualquer disciplina do semestre
    return AlunosMatriculados.objects.filter(aluno=aluno, turma__disciplina_semestre__semestre_id=semestre_id).exists()
