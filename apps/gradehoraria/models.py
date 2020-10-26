from django.db import models
from django.contrib.auth.models import User


class Disciplina(models.Model):
    id_disciplina = models.AutoField(primary_key=True)
    ds_disciplina = models.CharField(max_length=50, verbose_name="Descrição da Disciplina")
    sigla_disciplina = models.CharField(max_length=5, verbose_name="Sigla da Disciplina", unique=True)

    def __str__(self):
        return self.sigla_disciplina + ' - ' + self.ds_disciplina

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
    
    '''def __str__(self):
        return "%s (%s)" % (
            self.nm_professor,
            ", ".join(disciplinas.sigla_disciplina for disciplinas in self.disciplinas.all()),
        )'''
    class Meta:
        unique_together = ('matricula',)
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'
    '''def __str__(self):
        return "%s (%s)" % (self.nm_professor, ", ".join(disciplina.nm_disciplina for disciplina in self.disciplinas.all()))'''
    #def __str__(self):
    #    return self.nm_professor

class Horario(models.Model):
    SEMANA_CHOICES = (
        (1, 'Domingo-Feira'),
        (2, 'Segunda-Feira'),
        (3, 'Terça-Feira'),
        (4, 'Quarta-Feira'),
        (5, 'Quinta-Feira'),
        (6, 'Sexta-Feira'),
        (7, 'Sábado'),
    )
    HORARIO_CHOICES = (
        (1, '08:20 às 10:50'),
        (2, '11:10 às 12:40'),
        (3, '19:20 às 20:50'),
        (4, '21:10 às 22:50'),
    )
    TURNO_CHOICES = (
        (1, 'Matutino'),
        (2, 'Noturno'),
    )
    id_horario = models.AutoField(primary_key=True)
    dia_semana = models.IntegerField(verbose_name='Dia da semana', choices=SEMANA_CHOICES)
    horario = models.IntegerField(verbose_name='Horario', choices=HORARIO_CHOICES)
    turno = models.IntegerField(verbose_name='Turno', choices=TURNO_CHOICES)
    #def __str__(self):
     #   return self.get_dia_semana_display()

    class Meta:
        verbose_name_plural = 'Horários'
        unique_together = ['dia_semana', 'turno', 'horario']


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
    id_turma = models.AutoField(primary_key=True)
    ds_turma = models.CharField(max_length=20, verbose_name='Descrição da Turma', unique=True)
    semestre = models.IntegerField(verbose_name='Semestre', choices=SEMESTRE_CHOICES)

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
        return self.turma.ds_turma

    class Meta:
        unique_together = ['curso', 'turma', 'disciplina']


class Gene(models.Model):
    id_gene = models.AutoField(primary_key=True)
    cd_professor = models.ForeignKey(Professor, on_delete=models.CASCADE, verbose_name='cd_professor')
    cd_horario = models.ForeignKey(Horario, on_delete=models.CASCADE, verbose_name='cd_horario')
    cd_sala = models.ForeignKey(Sala, on_delete=models.CASCADE, verbose_name='cd_sala')
    oferta = models.OneToOneField(Oferta, on_delete=models.CASCADE, verbose_name='cd_gene')


class Grade(models.Model):
    id_grade = models.AutoField(primary_key=True)
    cd_gene = models.ForeignKey(Gene, on_delete=models.CASCADE, verbose_name='Gene')


class ParametrosGrade(models.Model):
    id_parametro = models.AutoField(primary_key=True)
    tamanhoPopulacao = models.IntegerField(verbose_name="População Inicial")
    numeroGeracoes = models.IntegerField(verbose_name="Qtd. máxima de tentativas")
    taxaMutacao = models.FloatField(verbose_name='Taxa de Mutação')
