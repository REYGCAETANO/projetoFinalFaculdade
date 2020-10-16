from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ProfessorForm, DisciplinaForm, CursoForm, TurmaForm, HorarioForm, OfertaForm, ParametrosGradeForm
from .models import Disciplina, Curso, Professor, Turma, Horario, Oferta, ParametrosGrade

import random
import itertools


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
def gradeHoraria(request):
    return render(request, 'gradehoraria.html', {})


def grade(request, professor, horario, sala):
    template_name = 'grades/nova_grade.html'


@login_required(login_url='/contas/login')
def adicionar_professor(request):
    template_name = 'professor/adicionar_professor.html'
    if request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Professor cadastrado com sucesso!')
            return redirect('gradehoraria:listar_professores')
        else:
            messages.warning(request, 'Erro ao cadastrar novo professor!')
    else:
        form = ProfessorForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login')
def listar_professores(request):
    templane_name = 'professor/listar_professores.html'
    professores = Professor.objects.all()
    context = {
        'professores': professores
    }
    return render(request, templane_name, context)

@login_required(login_url='/contas/login')
def editar_professor(request, id_professor):
    template_name = 'professor/adicionar_professor.html'
    context = {}
    editar_professor = get_object_or_404(Professor, id_professor=id_professor)
    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=editar_professor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados do professor alterados com sucesso!')
            return redirect('gradehoraria:listar_professores')
        else:
            messages.error(request, 'Erro ao alterar dados do professor')
    else:
        form = ProfessorForm(instance=editar_professor)
        context['form'] = form
        return render(request, template_name, context)


# FIXME: Criar confirmação de exclusão antes de persistir no banco - OK
@login_required(login_url='/contas/login')
def deleta_professor(request, id_professor):
    deleteProfessor = Professor.objects.get(id_professor=id_professor)
    deleteProfessor.delete()
    messages.warning(request, 'Professor excluído com sucesso!')
    return redirect('gradehoraria:listar_professores')


@login_required(login_url='/contas/login')
def adicionar_disciplina(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Disciplina cadastrada com sucesso!')
            return redirect('gradehoraria:listar_disciplinas')
        else:
            messages.error(request, 'Erro ao cadastrar disciplina!')
    else:
        if request.user.is_staff:
            form = DisciplinaForm()
            return render(request, 'disciplina/adicionar_disciplina.html', {'form': form})
        else:
            messages.error(request, 'Usuário sem permissão para cadastrar disciplinas!')
            return redirect('gradehoraria:listar_disciplinas')


@login_required(login_url='/contas/login')
def listar_disciplinas(request):
    disciplinas = Disciplina.objects.all()
    return render(request, 'disciplina/listar_disciplinas.html', {'disciplinas': disciplinas})


# FIXME: Criar confirmação de exclusão antes de persistir no banco - OK
@login_required(login_url='/contas/login')
def deleta_disciplina(request, id_disciplina):
    if request.user.is_staff:
        deleteDisciplina = Disciplina.objects.get(id_disciplina=id_disciplina).delete()
        messages.success(request, 'Disciplina excluída com sucesso!')
    else:
        messages.error(request, 'Você não pode excluir disciplinas.')
        return render(request, 'base.html')
    return redirect('gradehoraria:listar_disciplinas')


@login_required(login_url='/contas/login')
def editar_disciplina(request, id_disciplina):
    editar_disciplina = get_object_or_404(Disciplina, id_disciplina=id_disciplina)
    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=editar_disciplina)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados da disciplina alterados com sucesso!')
            return redirect('gradehoraria:listar_disciplinas')
        else:
            messages.error(request, 'Erro ao alterar dados da disciplina')
    else:
        form = DisciplinaForm(instance=editar_disciplina)
        return render(request, 'disciplina/adicionar_disciplina.html', {'form': form})


@login_required(login_url='/contas/login')
def adicionar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso cadastrado com sucesso!')
            return redirect('gradehoraria:listar_cursos')
        else:
            messages.error(request, 'Erro ao cadastrar o curso!')
    else:
        form = CursoForm()
    return render(request, 'curso/adicionar_curso.html', {'form': form})


@login_required(login_url='/contas/login')
def listar_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'curso/listar_cursos.html', {'cursos': cursos})


# FIXME: Criar confirmção de exclusão antes de persistir no banco
@login_required(login_url='/contas/login')
def deleta_curso(request, id_curso):
    deleteCurso = Curso.objects.get(id_curso=id_curso)
    deleteCurso.delete()
    messages.warning(request, 'Curso excluído com sucesso!')
    return redirect('gradehoraria:listar_cursos')


@login_required(login_url='/contas/login')
def editar_curso(request, id_curso):
    editarCurso = get_object_or_404(Curso, id_curso=id_curso)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=editarCurso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados do curso alterados com sucesso!')
            return redirect('gradehoraria:listar_cursos')
        else:
            messages.error(request, 'Erro ao alterar dados do curso!')
    else:
        form = CursoForm(instance=editarCurso)
        return render(request, 'curso/adicionar_curso.html', {'form': form})

@login_required(login_url='/contas/login')
def adicionar_turma(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Turma cadastrada com sucesso!')
            return redirect('gradehoraria:listar_turmas')
        else:
            messages.error(request, 'Erro ao cadastrar turma!')
    else:
        form = TurmaForm()
    return render(request, 'turma/adicionar_turma.html', {'form': form})


@login_required(login_url='/contas/login')
def listar_turmas(request):
    turmas = Turma.objects.all()
    return render(request, 'turma/listar_turmas.html', {'turmas': turmas})


# FIXME: Criar confirmação de exclusão antes de persistir no banco - OK
@login_required(login_url='/contas/login')
def deleta_turma(request, id_turma):
    deleteTurma = Turma.objects.get(id_turma=id_turma).delete()
    messages.success(request, 'Turma excluida com sucesso!')
    return redirect('gradehoraria:listar_turmas')


@login_required(login_url='/contas/login')
def editar_turma(request, id_turma):
    editar_turma = get_object_or_404(Turma, id_turma=id_turma)
    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=editar_turma)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados da turma alterado com sucesso!')
            return redirect('gradehoraria:listar_turmas')
        else:
            messages.error(request, 'Erro ao alterar dados da turma')
    else:
        form = TurmaForm(instance=editar_turma)
        return render(request, 'turma/adicionar_turma.html', {'form': form})



@login_required(login_url='/contas/login')
def adicionar_horario(request):
    if request.method == 'POST':
        form = HorarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horário cadastrado com sucesso!')
            return redirect('gradehoraria:listar_horarios')
        else:
            messages.error(request, 'Erro ao cadastrar turno!')
    else:
        form = HorarioForm()
    return render(request, 'horario/adicionar_horario.html', {'form': form})


@login_required(login_url='/contas/login')
def listar_horarios(request):
    horarios = Horario.objects.all()
    return render(request, 'horario/listar_horarios.html', {'horarios': horarios})


# FIXME: Criar confirmação de exclusão antes de persistir no banco
@login_required(login_url='/contas/login')
def deleta_horario(request, id_horario):
    deleteHorario = Horario.objects.get(id_horario=id_horario).delete()
    messages.success(request, 'Horário excluido com sucesso!')
    return redirect('gradehoraria:listar_horarios')


@login_required(login_url='/contas/login')
def editar_horario(request, id_horario):
    editar_horario = get_object_or_404(Horario, id_horario=id_horario)
    if request.method == 'POST':
        form = HorarioForm(request.POST, instance=editar_horario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados do Horário alterados com sucesso!')
            return redirect('gradehoraria:listar_horarios')
        else:
            messages.error(request, 'Erro ao alterar dados do horário')
    else:
        form = HorarioForm(instance=editar_turma)
        return render(request, 'horario/adicionar_horario.html', {'form': form})


@login_required(login_url='/contas/login')
def adicionar_oferta(request):
    if request.method == 'POST':
        form = OfertaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Oferta cadastrada com sucesso!')
            return redirect('gradehoraria:adicionar_oferta')
        else:
            messages.error(request, 'Erro ao cadastrar oferta! Oferta já cadastrada')
            return redirect('gradehoraria:listar_ofertas')
    else:
        if request.user.is_staff:
            form = OfertaForm()
            return render(request, 'oferta/adicionar_oferta.html', {'form': form})
        else:
            messages.error(request, 'Usuário sem permissão para cadastrar oferta!')
            return redirect('gradehoraria:listar_ofertas')


@login_required(login_url='/contas/login')
def listar_ofertas(request):
    ofertas = Oferta.objects.all()
    return render(request, 'oferta/listar_ofertas.html', {'ofertas': ofertas})


@login_required(login_url='/contas/login')
def adicionar_parametros(request):
    if request.method == 'POST':
        form = ParametrosGradeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Parâmetro cadastrada com sucesso!')
            return redirect('/')
        else:
            messages.error(request, 'Erro ao cadastrar oferta! Oferta já cadastrada')
            return redirect('/')
    else:
        if request.user.is_staff:
            form = ParametrosGradeForm()
            return render(request, 'grade/cadastrar_parametros.html', {'form': form})
        else:
            messages.error(request, 'Usuário sem permissão para cadastrar parâmetro!')
            return redirect('/')

@login_required(login_url='/contas/login')
def editar_parametros(request, id_parametro):
    editar_parametro = get_object_or_404(ParametrosGrade, id_parametro=id_parametro)
    if request.method == 'POST':
        form = ParametrosGradeForm(request.POST, instance=editar_parametro)
        if form.is_valid():
            f = form.save(commit=False)
            f.taxaMutacao = 0.5
            f.save()
            messages.success(request, 'Parâmetros alterados com sucesso!')
            return redirect('gradehoraria:listar_parametros')
        else:
            messages.error(request, 'Erro ao alterar os parâmetros')
    else:
        form = ParametrosGradeForm(instance=editar_parametro)
        return render(request, 'grade/cadastrar_parametros.html', {'form': form})

@login_required(login_url='/contas/login')
def listar_parametros(request):
    parametros = ParametrosGrade.objects.all()
    return render(request, 'grade/listar_parametros.html', {'parametros': parametros})