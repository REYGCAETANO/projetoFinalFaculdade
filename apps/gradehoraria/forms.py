from django import forms

from .models import Professor, Horario, Sala, Curso, Turma, Disciplina, Oferta, Grade, ParametrosGrade, Gene


class ProfessorForm(forms.ModelForm):
    # turno = forms.CharField(label="Turno", required=True)
    # disponibilidade = forms.CharField(label="disponibilidade", required=False)

    def listar_disciplinas(self, obj):
        return ", ".join(c.sigla_disciplina for c in obj.disciplinas.all())

    listar_disciplinas.short_description = "Disciplinas"

    class Meta:
        model = Professor
        fields = ('nm_professor', 'matricula', 'disciplinas')
        #fields = '__all__'


class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ('dia_semana', 'turno', 'horario')


class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = '__all__'


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'


class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = '__all__'
        #exclude = ['professor_id', 'disciplina_id']


class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = '__all__'


class OfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = '__all__'


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = '__all__'


class ParametrosGradeForm(forms.ModelForm):
    class Meta:
        model = ParametrosGrade
        exclude = ('taxaMutacao',)


class GeneForm(forms.ModelForm):
    class Meta:
        model = Gene
        fields = '__all__'