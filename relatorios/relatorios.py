from collections import defaultdict
import pandas as pd
from gestao.models import Semestre, DisciplinasSemestre, AlunosPendentes, AlunosMatriculados, Curso

def gerar_relatorio(semestre_id):
    # Buscar o semestre
    semestre = Semestre.objects.get(pk=semestre_id)

    # Filtrar as disciplinas do semestre
    disciplinas_semestre = DisciplinasSemestre.objects.filter(semestre=semestre)

    # Inicializar um dicionário para armazenar os dados do relatório
    relatorio_data = defaultdict(dict)

    # Iterar sobre as disciplinas do semestre
    for disciplina_semestre in disciplinas_semestre:
        disciplina = disciplina_semestre.disciplina
        disciplina_nome = disciplina.nome
        numero_semestre = disciplina.numero_semestre

        # Filtrar os alunos pendentes e matriculados para a disciplina
        alunos_pendentes = AlunosPendentes.objects.filter(disciplina_semestre=disciplina_semestre)
        alunos_matriculados = AlunosMatriculados.objects.filter(turma__disciplina_semestre=disciplina_semestre)

        # Contar o número de alunos pendentes e matriculados por ano de matrícula
        for aluno_pendente in alunos_pendentes:
            ano_matricula = int(str(aluno_pendente.aluno.matricula)[:4])
            relatorio_data[(disciplina_nome, numero_semestre)][(str(ano_matricula), 'Pendentes')] = \
                relatorio_data[(disciplina_nome, numero_semestre)].get((str(ano_matricula), 'Pendentes'), 0) + 1
            relatorio_data[(disciplina_nome, numero_semestre)][(str(ano_matricula), 'Matriculados')] = 0

        for alunos_matriculado in alunos_matriculados:
            ano_matricula = int(str(alunos_matriculado.aluno.matricula)[:4])
            relatorio_data[(disciplina_nome, numero_semestre)][(str(ano_matricula), 'Matriculados')] = \
                relatorio_data[(disciplina_nome, numero_semestre)].get((str(ano_matricula), 'Matriculados'), 0) + 1

        # Calcular o total de pendentes e matriculados para esta disciplina semestre
        total_pendentes_disciplina = sum(relatorio_data[(disciplina_nome, numero_semestre)].get((str(ano_matricula), 'Pendentes'), 0) for ano_matricula in range(2010, 2030))
        total_matriculados_disciplina = sum(relatorio_data[(disciplina_nome, numero_semestre)].get((str(ano_matricula), 'Matriculados'), 0) for ano_matricula in range(2010, 2030))
        relatorio_data[(disciplina_nome, numero_semestre)][('Total', 'Pendentes')] = total_pendentes_disciplina
        relatorio_data[(disciplina_nome, numero_semestre)][('Total', 'Matriculados')] = total_matriculados_disciplina

        if (total_pendentes_disciplina == 0 or total_matriculados_disciplina == 0):
            relatorio_data[(disciplina_nome, numero_semestre)][('Total', 'Porcentagem')] = f"0"
        else:
            relatorio_data[(disciplina_nome, numero_semestre)][('Total', 'Porcentagem')] = f"{round((total_matriculados_disciplina / total_pendentes_disciplina) * 100)}%"

        # Calcular o número de alunos do curso de SI e de outros cursos para esta disciplina semestre
        curso_si = Curso.objects.get(pk=1)
        alunos_si = sum(alunos_matriculado.aluno.curso == curso_si for alunos_matriculado in alunos_matriculados)
        alunos_outros = total_matriculados_disciplina - alunos_si
        relatorio_data[(disciplina_nome, numero_semestre)][('Total - Matriculas', 'SI')] = alunos_si
        relatorio_data[(disciplina_nome, numero_semestre)][('Total - Matriculas', 'Outros')] = alunos_outros

    # Transformar os dados em um DataFrame para facilitar a manipulação
    df = pd.DataFrame(relatorio_data).T.fillna(0)
    df = df.sort_index(level=[0, 1], axis=1)

    return df
