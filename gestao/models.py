from django.db import models

# Modelo Curso
class Curso(models.Model):
    codigo = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

# Modelo Aluno
class Aluno(models.Model):
    matricula = models.CharField(max_length=12, primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    situacao = models.BooleanField(default=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

# Modelo Disciplina
class Disciplina(models.Model):
    codigo = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

# Modelo Semestre
class Semestre(models.Model):
    codigo = models.AutoField(primary_key=True)
    numero =models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.numero}º Semestre - {self.curso}"

# Modelo DisciplinasSemestre
class DisciplinasSemestre(models.Model):
    codigo = models.AutoField(primary_key=True)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.semestre.numero}º Semestre - {self.disciplina.nome}"

# Modelo AlunosPendentes
class AlunosPendentes(models.Model):
    codigo = models.AutoField(primary_key=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    disciplina_semestre = models.ForeignKey(DisciplinasSemestre, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.disciplina_semestre.disciplina.nome}º Semestre - {self.aluno.nome}"
