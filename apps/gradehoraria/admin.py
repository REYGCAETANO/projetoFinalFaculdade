from django.contrib import admin
from .models import Curso, Turma, Disciplina, Professor, Sala, Horario, Oferta, Gene


def grade(modeladmin, request, queryset):
    queryset.count()
grade.short_description = "Gerar"


class CursoAdmin(admin.ModelAdmin):
    list_display = ['nm_curso', 'sigla_curso']
    actions = [grade]


class DisciplinaAdmin(admin.ModelAdmin):
    pass


class HorarioAdmin(admin.ModelAdmin):
    list_display = ['dia_semana', 'horario', 'turno']
    list_filter = ['turno']
    ordering = ['id_horario']


class ProfessorAdmin(admin.ModelAdmin):
    pass


class SalaAdmin(admin.ModelAdmin):
    pass


class TurmaAdmin(admin.ModelAdmin):
    pass


class OfertaAdmin(admin.ModelAdmin):
    list_display = ['curso', 'turma', 'disciplina']
    actions = [grade]

class GradeAdmin(admin.ModelAdmin):
    pass

class GeneAdmin(admin.ModelAdmin):
    pass

admin.site.register(Curso, CursoAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(Disciplina, DisciplinaAdmin)
admin.site.register(Horario, HorarioAdmin)
admin.site.register(Sala, SalaAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Oferta, OfertaAdmin)
admin.site.register(Gene, GradeAdmin)