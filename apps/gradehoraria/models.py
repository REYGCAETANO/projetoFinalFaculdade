from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Disciplina(models.Model):
    id_disciplina = models.AutoField(primary_key=True)
    ds_disciplina = models.CharField(max_length=50, verbose_name="Descrição da Disciplina")
    sigla_disciplina = models.CharField(max_length=5, verbose_name="Sigla da Disciplina", unique=True)

    def __str__(self):
        return self.sigla_disciplina + ' - ' + self.ds_disciplina

    def listar_disciplinas(self, obj):
        return ", ".join(c.sigla_disciplina for c in obj.disciplinas.all())

    def save(self, force_insert=False, force_update=False):
        self.ds_disciplina = self.ds_disciplina.upper()
        super(Disciplina, self).save(force_insert, force_update)

    # objects = DisciplinaFiltros()


class Professor(models.Model):
    id_professor = models.AutoField(primary_key=True)
    nm_professor = models.CharField(max_length=100, verbose_name='Nome', unique=True)
    matricula = models.CharField(max_length=50, verbose_name='Matrícula', unique=True)
    disciplinas = models.ManyToManyField(Disciplina, related_name='professor_disciplina', verbose_name='Disciplina')
    # turno = models.CharField(max_length=20, verbose_name='Turno', choices=TURNO_CHOICES)

    def save(self, force_insert=False, force_update=False):
        self.nm_professor = self.nm_professor.upper()
        super(Professor, self).save(force_insert, force_update)

    def __str__(self):
        nome = str(self.nm_professor).strip().split()
        return nome[0] + ' ' + nome[len(nome)-1]

    # def list_disciplinas(self):
    #     return ", ".join([c.sigla_disciplina for c in self.disciplinas.all()])
    # list_disciplinas.short_description = "Disciplinas"

    # def listar_disciplinas(self):
    #     nome = str(self.nm_professor).strip().split()
    #     return "%s (%s)" % (
    #         nome[0] + ' ' + nome[len(nome)-1],
    #         ", ".join(disciplinas.sigla_disciplina for disciplinas in self.disciplinas.all()),
    #     )

    class Meta:
        unique_together = ('matricula',)
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'
    # def __str__(self):
    #     return "%s (%s)" % (self.nm_professor, ", ".join(disciplina.nm_disciplina for disciplina in self.disciplinas.all()))


class Horario(models.Model):
    HORARIO_CHOICES = (
        (1, '1 - Horário'),
        (2, '2 - Horário'),
        (3, '3 - Horário'),
        (4, '4 - Horário'),
        (5, '5 - Horário'),
        (6, '6 - Horário'),
        (7, '7 - Horário'),
        (8, '8 - Horário'),
        (9, '9 - Horário'),
        (10, '10 - Horário'),
        (11, '11 - Horário'),
        (12, '12 - Horário'),
    )
    id_horario = models.AutoField(primary_key=True)
    horario = models.IntegerField(verbose_name='Horário', choices=HORARIO_CHOICES)

    def __str__(self):
        horario = str(self.get_horario_display())
        return horario


class Sala(models.Model):
    id_sala = models.AutoField(primary_key=True)
    ds_sala = models.CharField(max_length=20, verbose_name='Sala', unique=True)
    andar = models.CharField(max_length=2, verbose_name='Andar')

    def __str__(self):
        return self.ds_sala


class Curso(models.Model):
    id_curso = models.AutoField(primary_key=True)
    nm_curso = models.CharField(max_length=50, verbose_name="Nome do Curso", unique=True)
    sigla_curso = models.CharField(max_length=5, verbose_name="Sigla do Curso", unique=True)

    def __str__(self):
        return self.nm_curso

    def save(self, force_insert=False, force_update=False):
        self.nm_curso = self.nm_curso.upper()
        self.sigla_curso = self.sigla_curso.upper()
        super(Curso, self).save(force_insert, force_update)


class Turma(models.Model):
    SEMESTRE_CHOICES = (
        (1, '1º Semestre'),
        (2, '2º Semestre'),
        (3, '3º Semestre'),
        (4, '4º Semestre'),
        (5, '5º Semestre'),
        (6, '6º Semestre'),
        (7, '7º Semestre'),
        (8, '8º Semestre'),
        (9, '9º Semestre'),
        (10, '10ºSemestre'),
    )
    TURNO_CHOICES = (
        (1, 'Matutino'),
        (2, 'Vespertino'),
        (3, 'Noturno'),
    )
    id_turma = models.AutoField(primary_key=True)
    ds_turma = models.CharField(max_length=20, verbose_name='Descrição da Turma', unique=True)
    semestre = models.IntegerField(verbose_name='Semestre', choices=SEMESTRE_CHOICES)
    turno = models.IntegerField(verbose_name='Turno', choices=TURNO_CHOICES)


    def __str__(self):
        return self.ds_turma

    '''def save(self, force_insert=False, force_update=False):
        self.ds_turma = self.ds_turma.upper()
        super(Turma, self).save(force_insert, force_update)'''
    # class Meta:
    #     unique_together = ('turma',)


class Oferta(models.Model):
    id_oferta = models.AutoField(primary_key=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, verbose_name='Curso')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name='Turma')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, verbose_name='Disciplina')

    def __str__(self):
        return self.disciplina.sigla_disciplina

    class Meta:
        unique_together = ['curso', 'turma', 'disciplina']


class Gene(models.Model):
    gene_id = models.AutoField(primary_key=True)
    cd_turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name='Turma')
    cd_professor = models.ForeignKey(Professor, on_delete=models.CASCADE, verbose_name='Professor')
    cd_horario = models.ForeignKey(Horario, on_delete=models.CASCADE, verbose_name='Horário')
    cd_sala = models.ForeignKey(Sala, on_delete=models.CASCADE, verbose_name='Sala')
    cd_oferta = models.OneToOneField(Oferta, on_delete=models.CASCADE, verbose_name='Oferta')
    # cd_geracao = models.IntegerField(verbose_name='Geração')

    class Meta:
        unique_together = ['cd_turma', 'cd_professor', 'cd_horario', 'cd_sala', 'cd_oferta']

class Grade(models.Model):
    id_grade = models.AutoField(primary_key=True)
    cd_turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name='Turma')
    cd_geracao = models.IntegerField(verbose_name='Geração')
    # data_criacao = models.DateTimeField(default=timezone.now)

class ParametrosGrade(models.Model):
    id_parametro = models.AutoField(primary_key=True)
    tamanhoPopulacao = models.IntegerField(verbose_name="População Inicial")
    numeroGeracoes = models.IntegerField(verbose_name="Qtd. máxima de tentativas")
    taxaMutacao = models.FloatField(verbose_name='Taxa de Mutação')
    paramTurma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name='Turma')
