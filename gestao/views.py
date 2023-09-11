from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.forms import modelformset_factory
from django.views.generic.edit import CreateView

from .models import *
from .forms import *

class ListaCursosView(View):
    template_name = 'lista_cursos.html'

    def get(self, request):
        cursos = Curso.objects.all()
        context = {'cursos': cursos}
        return render(request, self.template_name, context)

class DetalhesCursoView(View):
    template_name = 'detalhes_curso.html'

    def get(self, request, curso_codigo):
        curso = Curso.objects.get(codigo=curso_codigo)
        alunos = Aluno.objects.filter(curso=curso)
        context = {'curso': curso, 'alunos': alunos}
        return render(request, self.template_name, context)

class ListaSemestresView(View):
    template_name = 'lista_semestres.html'

    def get(self, request, curso_codigo):
        curso = Curso.objects.get(codigo=curso_codigo)
        semestres = Semestre.objects.filter(curso=curso)
        context = {'semestres': semestres, 'curso': curso}
        return render(request, self.template_name, context)

class PreencherDisciplinasSemestreView(View):
    template_name = 'preencher_disciplinas_semestre.html'

    def get(self, request, curso_codigo, semestre_codigo):
        semestre = Semestre.objects.get(pk=semestre_codigo)
        curso = Curso.objects.get(pk=curso_codigo)

        disciplinas_selecionadas = DisciplinasSemestre.objects.filter(semestre=semestre)

        disciplinas_selecionadas_ids = [disciplina.disciplina.codigo for disciplina in disciplinas_selecionadas]

        form = PreencherDisciplinasSemestreForm(initial={'disciplinas': disciplinas_selecionadas_ids})
        context = {'form': form, 'curso': curso, 'semestre': semestre}
        return render(request, self.template_name, context)

    def post(self, request, curso_codigo, semestre_codigo):
        semestre = get_object_or_404(Semestre, codigo=semestre_codigo)
        curso = Curso.objects.get(pk=curso_codigo)
        form = PreencherDisciplinasSemestreForm(request.POST)
        if form.is_valid():
            # Salvar as disciplinas associadas ao semestre
            disciplinas_selecionadas = form.cleaned_data['disciplinas']
            DisciplinasSemestre.objects.filter(semestre=semestre).delete()  # Limpar as seleções anteriores
            for disciplina in disciplinas_selecionadas:
                DisciplinasSemestre.objects.create(semestre=semestre, disciplina=disciplina)
            return redirect('lista_semestres', curso_codigo=curso.codigo)  # Redirecionar após a conclusão do processo

        context = {'form': form, 'curso': curso, 'semestre': semestre}
        return render(request, self.template_name, context)

class PreencherAlunosPendentesView(View):
    template_name = 'gerar_alunos_pendentes.html'

    def get(self, request, curso_codigo, semestre_codigo):
        # Recupere o semestre com base no código fornecido
        semestre = Semestre.objects.get(curso__codigo=curso_codigo, codigo=semestre_codigo)

        # Recupere as disciplinas associadas a este semestre
        disciplinas_semestre = DisciplinasSemestre.objects.filter(semestre=semestre)

        # Crie um dicionário para armazenar os formulários para cada disciplina
        forms = {}
        for disciplina_semestre in disciplinas_semestre:
            # Use a disciplina_semestre como chave e o formulário como valor
            forms[disciplina_semestre.pk] = AlunosPendentesForm()

        context = {
            'curso_codigo': curso_codigo,
            'semestre_codigo': semestre_codigo,
            'forms': forms,
            'disciplinas_semestre': disciplinas_semestre,
        }
        return render(request, self.template_name, context)

    def post(self, request, curso_codigo, semestre_codigo):
        # Recupere o semestre com base no código fornecido
        semestre = Semestre.objects.get(curso__codigo=curso_codigo, codigo=semestre_codigo)

        # Recupere as disciplinas associadas a este semestre
        disciplinas_semestre = DisciplinasSemestre.objects.filter(semestre=semestre)

        AlunosPendentes.objects.filter(disciplina_semestre__in=disciplinas_semestre).delete()

        # Processar os formulários postados
        for disciplina_semestre in disciplinas_semestre:
            form = AlunosPendentesForm(request.POST)
            if form.is_valid():
                matriculas = form.cleaned_data['matriculas'].split('\n')
                for matricula in matriculas:
                    matricula = matricula.strip()  # Remova espaços em branco
                    if matricula:
                        aluno, created = Aluno.objects.get_or_create(matricula=matricula)
                        AlunosPendentes.objects.get_or_create(
                            aluno=aluno,
                            disciplina_semestre=disciplina_semestre
                        )

        return redirect('lista_semestres', curso_codigo=curso_codigo)
    
class CriarSemestreView(View):
    template_name = 'criar_semestre.html'

    def get(self, request, curso_codigo):
        curso = Curso.objects.get(codigo=curso_codigo)
        form = CriarSemestreForm()
        context = {'form': form, 'curso': curso}
        return render(request, self.template_name, context)

    def post(self, request, curso_codigo):
        curso = Curso.objects.get(codigo=curso_codigo)
        form = CriarSemestreForm(request.POST)

        if form.is_valid():
            novo_semestre = form.save(commit=False)
            novo_semestre.curso = curso
            novo_semestre.save()

            return redirect('detalhes_curso', curso_codigo=curso.codigo)

        context = {'form': form, 'curso': curso}
        return render(request, self.template_name, context)

class InserirAlunosCursoView(View):
    template_name = 'inserir_alunos_curso.html'

    def get(self, request, curso_codigo):
        curso = Curso.objects.get(codigo=curso_codigo)
        return render(request, self.template_name, {'curso': curso})

    def post(self, request, curso_codigo):
        curso = Curso.objects.get(codigo=curso_codigo)
        lista_alunos = request.POST.get('lista_alunos')

        if lista_alunos:
            # Primeiro, exclua todos os alunos associados a este curso
            Aluno.objects.filter(curso=curso).delete()

            # Processar a lista de alunos e criar registros de Aluno com base na lista
            for linha in lista_alunos.split('\n'):
                matricula, nome, email = linha.strip().split(',')
                Aluno.objects.create(
                    matricula=matricula,
                    nome=nome,
                    email=email,
                    curso=curso
                )

        return redirect('detalhes_curso', curso_codigo=curso.codigo)
    
class InserirDisciplinasCursoView(View):
    template_name = 'inserir_disciplinas_curso.html'

    def get(self, request, curso_codigo):
        curso = Curso.objects.get(codigo=curso_codigo)
        return render(request, self.template_name, {'curso': curso})

    def post(self, request, curso_codigo):
        curso = Curso.objects.get(codigo=curso_codigo)
        lista_disciplinas = request.POST.get('lista_disciplinas')

        if lista_disciplinas:
            # Primeiro, exclua todos os alunos associados a este curso
            Disciplina.objects.filter(curso=curso).delete()

            # Processar a lista de alunos e criar registros de Aluno com base na lista
            for linha in lista_disciplinas.split('\n'):
                if linha:
                    Disciplina.objects.create(nome=linha, curso=curso)

        return redirect('detalhes_curso', curso_codigo=curso.codigo)
    
class InserirProfessoresCursoView(View):
    template_name = 'inserir_professores_curso.html'

    def get(self, request, curso_codigo):
        curso = Curso.objects.get(codigo=curso_codigo)
        return render(request, self.template_name, {'curso': curso})

    def post(self, request, curso_codigo):
        curso = Curso.objects.get(codigo=curso_codigo)
        lista_professores = request.POST.get('lista_professores')

        if lista_professores:
            # Primeiro, exclua todos os alunos associados a este curso
            Professor.objects.filter(curso=curso).delete()

            # Processar a lista de alunos e criar registros de Aluno com base na lista
            for linha in lista_professores.split('\n'):
                if linha:
                    Professor.objects.create(nome=linha, curso=curso)

        return redirect('detalhes_curso', curso_codigo=curso.codigo)
    
class PreencherTurmasView(View):
    template_name = 'preencher_turmas.html'

    def get(self, request, curso_codigo, semestre_codigo):
        # Recupere as disciplinas do semestre
        curso = Curso.objects.get(codigo=curso_codigo)
        semestre = Semestre.objects.get(codigo=semestre_codigo)
        disciplinas_semestre = DisciplinasSemestre.objects.filter(semestre__pk=semestre_codigo)

        # Crie o formulário com base nas disciplinas do semestre
        form = PreencherTurmasForm(disciplinas_semestre=disciplinas_semestre)

        context = {'form': form, 'curso': curso, 'semestre': semestre}
        return render(request, self.template_name, context)

    def post(self, request, curso_codigo, semestre_codigo):
        curso = Curso.objects.get(codigo=curso_codigo)
        semestre = Semestre.objects.get(codigo=semestre_codigo)
        disciplinas_semestre = DisciplinasSemestre.objects.filter(semestre__pk=semestre_codigo)

        form = PreencherTurmasForm(request.POST, disciplinas_semestre=disciplinas_semestre)

        if form.is_valid():
            Turma.objects.filter(disciplina_semestre__in=disciplinas_semestre).delete()

            for disciplina_semestre in disciplinas_semestre:
                num_turmas = form.cleaned_data[f'num_turmas_{disciplina_semestre.pk}']
                for i in range(1, num_turmas + 1):
                    Turma.objects.create(
                        disciplina_semestre=disciplina_semestre,
                        professor=None
                    )

            return redirect('preencher_disciplinas', curso_codigo, semestre_codigo)

        context = {'form': form, 'curso': curso, 'semestre': semestre}
        return render(request, self.template_name, context)
    
class EscolherProfessoresView(View):
    template_name = 'escolher_professores.html'

    def get(self, request, curso_codigo, semestre_codigo):
        # Obtenha todas as turmas do semestre
        curso = Curso.objects.get(codigo=curso_codigo)
        semestre = Semestre.objects.get(codigo=semestre_codigo)
        turmas = Turma.objects.filter(disciplina_semestre__semestre__codigo=semestre_codigo)
        professores = Professor.objects.filter(curso=curso)
        professores_turmas = {}
        for turma in turmas:
            professores_turmas[turma.pk] = turma.professor_id
        
        context = {'turmas': turmas, 'professores': professores, 'curso': curso, 'semestre': semestre, 'professores_turmas': professores_turmas}
        return render(request, self.template_name, context)

    def post(self, request, curso_codigo, semestre_codigo):
        # Obtenha todas as turmas do semestre
        curso = Curso.objects.get(codigo=curso_codigo)
        semestre = Semestre.objects.get(codigo=semestre_codigo)
        turmas = Turma.objects.filter(disciplina_semestre__semestre__codigo=semestre_codigo)

        # Para cada turma, obtenha o ID do professor selecionado no formulário
        for turma in turmas:
            professor_id = request.POST.get(f'professor_{turma.pk}')

            # Atualize o professor da turma com base no ID selecionado
            if professor_id:
                professor = Professor.objects.get(pk=professor_id)
                turma.professor = professor
                turma.save()

        # Redirecione para onde você desejar após atribuir os professores
        return redirect('preencher_disciplinas', curso_codigo, semestre_codigo)

class PreencherAlunosMatriculadosView(View):
    template_name = 'gerar_alunos_matriculados.html'

    def get(self, request, curso_codigo, semestre_codigo):
        # Recupere o semestre com base no código fornecido

        semestre = Semestre.objects.get(curso__codigo=curso_codigo, codigo=semestre_codigo)

        # Recupere as disciplinas associadas a este semestre
        turmas = Turma.objects.filter(disciplina_semestre__semestre=semestre)

        # Crie um dicionário para armazenar os formulários para cada disciplina
        forms = {}
        for turma in turmas:
            # Use a disciplina_semestre como chave e o formulário como valor
            forms[turma.pk] = AlunosMatriculadosForm()

        context = {
            'curso_codigo': curso_codigo,
            'semestre_codigo': semestre_codigo,
            'forms': forms,
            'turmas': turmas,
        }
        return render(request, self.template_name, context)

    def post(self, request, curso_codigo, semestre_codigo):
        # Recupere o semestre com base no código fornecido
        semestre = Semestre.objects.get(curso__codigo=curso_codigo, codigo=semestre_codigo)

        # Recupere as disciplinas associadas a este semestre
        turmas = Turma.objects.filter(disciplina_semestre__semestre=semestre)

        AlunosMatriculados.objects.filter(turma__in=turmas).delete()

        # Processar os formulários postados
        for turma in turmas:
            form = AlunosMatriculadosForm(request.POST)
            if form.is_valid():
                matriculas = form.cleaned_data['matriculas'].split('\n')
                for matricula in matriculas:
                    matricula = matricula.strip()  # Remova espaços em branco
                    if matricula:
                        aluno, created = Aluno.objects.get_or_create(matricula=matricula)
                        AlunosMatriculados.objects.get_or_create(
                            aluno=aluno,
                            turma=turma
                        )

        return redirect('preencher_disciplinas', curso_codigo=curso_codigo, semestre_codigo=semestre_codigo)