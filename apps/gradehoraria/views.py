from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from more_itertools import unique_everseen
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection

from .forms import ProfessorForm, DisciplinaForm, CursoForm, TurmaForm, HorarioForm, SalaForm, OfertaForm, ParametrosGradeForm, GeneForm
from .models import Disciplina, Curso, Professor, Turma, Horario, Sala, Oferta, ParametrosGrade, Gene

import random
import itertools


@staff_member_required(login_url='/')
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
    professores = Professor.objects.prefetch_related('disciplinas')

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
        messages.warning(request, 'Disciplina excluída com sucesso!')
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
    messages.warning(request, 'Turma excluída com sucesso!')
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
def adicionar_sala(request):
    if request.method == 'POST':
        form = SalaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sala cadastrada com sucesso!')
            return redirect('gradehoraria:listar_salas')
        else:
            messages.error(request, 'Erro ao cadastrar sala!')
    else:
        form = SalaForm()
    return render(request, 'sala/adicionar_sala.html', {'form': form})


@login_required(login_url='/contas/login')
def listar_salas(request):
    salas = Sala.objects.all()
    return render(request, 'sala/listar_salas.html', {'salas': salas})


# FIXME: Criar confirmação de exclusão antes de persistir no banco - OK
@login_required(login_url='/contas/login')
def deleta_sala(request, id_sala):
    deleteSala = Sala.objects.get(id_sala=id_sala).delete()
    messages.warning(request, 'Sala excluída com sucesso!')
    return redirect('gradehoraria:listar_salas')


@login_required(login_url='/contas/login')
def editar_sala(request, id_sala):
    editar_sala = get_object_or_404(Sala, id_sala=id_sala)
    if request.method == 'POST':
        form = SalaForm(request.POST, instance=editar_sala)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados da sala alterado com sucesso!')
            return redirect('gradehoraria:listar_salas')
        else:
            messages.error(request, 'Erro ao alterar dados da sala')
    else:
        form = SalaForm(instance=editar_sala)
        return render(request, 'sala/adicionar_sala.html', {'form': form})


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
    messages.warning(request, 'Horário excluido com sucesso!')
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
        form = HorarioForm(instance=editar_horario)
        return render(request, 'horario/adicionar_horario.html', {'form': form})


@login_required(login_url='/contas/login')
def adicionar_oferta(request):
    if request.method == 'POST':
        form = OfertaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Oferta cadastrada com sucesso!')
            return redirect('gradehoraria:listar_ofertas')
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
def listar_ofertas(request, turma=-1):
    turmas = Turma.objects.all()
    if turma==-1:
        ofertas = Oferta.objects.all().order_by('id_oferta')
    else:
        ofertas = Oferta.objects.filter(turma_id=turma)
    return render(request, 'oferta/listar_ofertas.html', {'ofertas': ofertas, 'turmas': turmas})


@login_required(login_url='/contas/login')
def editar_oferta(request, id_oferta):
    id_oferta = get_object_or_404(Oferta, id_oferta=id_oferta)
    if request.method == 'POST':
        form = OfertaForm(request.POST, instance=id_oferta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados da oferta alterados com sucesso!')
            return redirect('gradehoraria:listar_ofertas')
        else:
            messages.error(request, 'Erro ao alterar dados da oferta!')
            return redirect('gradehoraria:listar_ofertas')
    else:
        form = OfertaForm(instance=id_oferta)
        return render(request, 'oferta/adicionar_oferta.html', {'form': form})


@login_required(login_url='/contas/login')
def deleta_oferta(request, id_oferta):
    deleteOferta = Oferta.objects.get(id_oferta=id_oferta).delete()
    messages.warning(request, 'Oferta excluída com sucesso!')
    return redirect('gradehoraria:listar_ofertas')


@login_required(login_url='/contas/login')
def adicionar_parametros(request):
    if request.method == 'POST':
        form = ParametrosGradeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Parâmetro cadastrada com sucesso!')
            return redirect('/')
        else:
            messages.error(request, 'Erro ao cadastrar parâmetro! ')
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


class Geneg():
    def __init__(self, professor, horario, sala, oferta=0):
        self.professor = professor
        self.horario = horario
        self.sala = sala
        self.oferta = oferta


class Individuo():

    def __init__(self, geracao=0):
        self.parametros = ParametrosGrade.objects.get(pk=1)
        self.ofertas = Oferta.objects.filter(turma_id=self.parametros.paramTurma_id).order_by('id_oferta')
        self.tamanhoCromossomo = self.ofertas.count()
        self.notaAvaliacao = 0
        self.geracao = geracao
        self.cromossomo = []
        self.melhorCromossomo = []

        horarios = Horario.objects.all()
        salas = Sala.objects.all()
        #def
        # for j in self.ofertas:
        #     professor = random.choice(Professor.objects.filter(disciplinas=j.disciplina_id))
        #     self.cromossomo.append(Geneg(professor, random.choice(horarios), random.choice(salas)))

        for j in self.ofertas:
            try:
                professor = random.choice(Professor.objects.filter(disciplinas=j.disciplina_id))
                self.cromossomo.append(Geneg(professor, random.choice(horarios), random.choice(salas)))

            # except UnboundLocalError as ue:
            #     print("")

            except Exception as e:
                print(" Professor: %s Disciplina: %s"% (professor.nm_professor, j.disciplina_id))

    def validacaoParametros(self):

        if self.tamanhoCromossomo == 0:
            return "Nenhuma oferta foi cadastrada para essa turma"


    def cromossomoMelhorSolucao (self, cromossomo):
        for g in cromossomo:
            disciplinas = random.choice(Disciplina.objects.filter(professor_disciplina__id_professor=g.professor.id_professor))

            try:
                ofertaFinal = self.ofertas.get(disciplina_id=disciplinas.id_disciplina)
                self.melhorCromossomo.append(Geneg(g.professor, g.horario, g.sala, ofertaFinal))

            except Oferta.DoesNotExist:
                continue
            # for d in Disciplina.objects.filter(professor_disciplina__id_professor=g.professor.id_professor):
            #     try:
            #         ofertaFinal = self.ofertas.get(disciplina_id=d.id_disciplina)
            #         self.melhorCromossomo.append(Geneg(g.professor, g.horario, g.sala, ofertaFinal))
            #
            #     except Oferta.DoesNotExist:
            #         continue
        return self.melhorCromossomo

            # professores = Professor.objects.prefetch_related('disciplinas').filter(id_professor=g.professor.id_professor)
            # ofertaFinaTeste = self.ofertas.get(disciplina_id=6)
            # self.cromossomo.append(Geneg(j.professor, j.horario, j.sala, ofertaFinal))

    # def avaliacao(self):
    #     nota = 0
    #     for i, j in itertools.combinations(self.cromossomo, 2):
    #         if i.horario == j.horario and i.professor == j.professor:
    #             nota += 10
    #         if i.sala == j.sala and i.horario == j.horario:
    #             nota += 10
    #     self.notaAvaliacao = nota

    def crossover(self, other):
        corte = random.randint(0, self.tamanhoCromossomo)
        cromossomo1 = self.cromossomo[0:corte] + other.cromossomo[corte::]
        cromossomo2 = other.cromossomo[0:corte] + self.cromossomo[corte::]
        filho1 = Individuo(self.geracao + 1)
        filho1.cromossomo = cromossomo1
        filho2 = Individuo(self.geracao + 1)
        filho2.cromossomo = cromossomo2
        return [filho1, filho2]

    def mutacao(self, cromossomo, taxaMutacao):
        for i in range(self.tamanhoCromossomo):
            if random.random() < taxaMutacao:
                pos1 = round(random.random() * self.tamanhoCromossomo - 1)
                pos2 = round(random.random() * self.tamanhoCromossomo - 1)
                val1 = cromossomo[pos1]
                val2 = cromossomo[pos2]
                cromossomo[pos1] = val2
                cromossomo[pos2] = val1
        return self

class AlgoritmoGenetico():

    def __init__(self, parametros):
        self.parametros = parametros
        self.tamanhoPopulacao = parametros.tamanhoPopulacao
        self.populacao = []
        self.geracao = 0
        self.melhorSolucao = -1
        # self.ofertas = []
        self.cromossomoMelhorSolucao = []
        self.ofertas = Oferta.objects.filter(turma_id=self.parametros.paramTurma_id)
        self.geracaoFinal = 0

    def inicializaPopulacao(self):
        for i in range(self.tamanhoPopulacao):
            self.populacao.append(Individuo())
        self.melhorSolucao = self.populacao[0]

    def avaliacao(self, populacao):
        nota = 0
        for p in populacao:
            for i, j in itertools.combinations(p.cromossomo, 2):
                if i.horario == j.horario and i.professor == j.professor:
                    nota += 10
                if i.sala == j.sala and i.horario == j.horario:
                    nota += 10
            p.notaAvaliacao = nota

    def avaliacaoMelhorSolucao(self, cromossomo):
        nota = 0
        ofertas = []

        try:
            for g in cromossomo:
                ofertas.append(g.oferta.id_oferta)
                resultado = list(unique_everseen(ofertas))
            if self.ofertas.count() != len(resultado):
                nota += 100
            return nota

        except UnboundLocalError as ue:
            print("Não existe ofertas cadastrada para essa turma %s" %self.parametros.paramTurma_id)
            raise

    def ordenaPopulacao(self):
        self.populacao = sorted(self.populacao,
                                key=lambda populacao: populacao.notaAvaliacao,
                                reverse=False)

    def     melhorIndividuo(self, individuo):
        if individuo.notaAvaliacao < self.melhorSolucao.notaAvaliacao:
            self.melhorSolucao = individuo

    def selecionaPai(self, populacao):
        taxaPopulacao = int(self.tamanhoPopulacao * 0.5)
        return populacao[0:taxaPopulacao]

    def visualizaGeracao(self):
        melhorSolucao = self.populacao[0]
        print("G: %s -> Valor: %s" % (melhorSolucao.geracao,
                                      melhorSolucao.notaAvaliacao))
        self.geracaoFinal = melhorSolucao.geracao

    def resolver(self, numeroGeracoes,  taxaMutacao):
        self.inicializaPopulacao()
        Individuo().validacaoParametros()
        self.avaliacao(self.populacao)
        self.ordenaPopulacao()

        for geracao in range(numeroGeracoes):
            pop_temp = self.selecionaPai(self.populacao)
            self.populacao = []
            for i in self.populacao:
                i.geracao = i.geracao + 1

            for i in range(0, self.tamanhoPopulacao, 2):
                pais = random.choices(pop_temp, k=2)
                self.populacao.extend(pais[0].crossover(pais[1]))

            for i in self.populacao:
                i.mutacao(i.cromossomo, taxaMutacao)

            self.avaliacao(self.populacao)
            self.ordenaPopulacao()
            self.visualizaGeracao()
            self.melhorIndividuo(self.populacao[0])
            if self.melhorSolucao.notaAvaliacao == 0:
                self.cromossomoMelhorSolucao = Individuo().cromossomoMelhorSolucao(self.melhorSolucao.cromossomo)
                if self.avaliacaoMelhorSolucao(self.cromossomoMelhorSolucao) == 0:
                    print("Melhor Solução -> G: %s \nNota: %s \nCromossomo: %s \ncromossomoMelhorSolucao: %s" %
                          # (self.melhorSolucao.geracao,
                          (self.geracaoFinal,
                           self.melhorSolucao.notaAvaliacao,
                           self.melhorSolucao.cromossomo,
                           self.cromossomoMelhorSolucao,))
                    return self.cromossomoMelhorSolucao, self.geracaoFinal+1


# FIXME: Criar exception para quando o tamanho do cromossomo for superior a quantidade de aulas na semana
# FIXME: Carregar o tamanho do cromossomo da base de dados.
@login_required(login_url='/contas/login')
def gerarGradeHoraria(request):
    try:
        parametros = ParametrosGrade.objects.get(pk=1)
        turma = Turma.objects.get(id_turma=parametros.paramTurma_id)
        ofertas = Oferta.objects.filter(turma_id=parametros.paramTurma_id).count()

        if ofertas > 12:
            messages.error(request, "Existem %s ofertas cadastrada para essa turma. Limite máximo 12 ofertas" %ofertas, turma.ds_turma)
            return redirect('gradehoraria:listar_ofertas', turma.id_turma)
        ag = AlgoritmoGenetico(parametros)
        resultado = ag.resolver(parametros.numeroGeracoes, parametros.taxaMutacao)

        # gene = Gene.objects.select_related('cd_professor').select_related('cd_horario').select_related('cd_sala')
        #professor = random.choices(Professor.objects.prefetch_related('disciplinas').filter(disciplinas=7))

        '''for gene in resultado[0]:
            g = Gene.objects.create(cd_professor_id=gene.professor,
                                    cd_horario_id=gene.horario,
                                    cd_sala_id=gene.sala,
                                    oferta_id=Oferta.objects.select_related('disciplina').prefetch_related('disciplina').get(turma_id=parametros.paramTurma_id))

            g.save'''

        for gene in resultado[0]:
            g = Gene.objects.create(cd_professor_id=gene.professor.id_professor,
                                    cd_horario_id=gene.horario.id_horario,
                                    cd_sala_id=gene.sala.id_sala,
                                    oferta_id=gene.oferta.id_oferta)

            g.save

        return render(request, 'grade/gerar_grade.html', {'resultado': resultado[0], 'geracao': resultado[1]})
    except UnboundLocalError:
        messages.error(request, "Não existe ofertas cadastrada para a turma - %s" %turma.ds_turma)
        return redirect('gradehoraria:listar_parametros')
    # except TypeError:
    #     messages.error(request, "Não foi encontrado uma solução para o problema. Mude os parâmetros ou gere a grade novamente.")
    #     return redirect('gradehoraria:listar_parametros')
    except Exception as e:
        messages.error(request, e.with_traceback())
        return redirect('gradehoraria:listar_parametros')


# def salvarGradeHoraria(resultado):
#
#     for gene in resultado:
#         g = Gene.objects.create(cd_professor_id=gene.professor,
#                                 cd_horario_id=gene.horario,
#                                 cd_sala_id=gene.sala,
#                                 oferta_id=Oferta.oferta.id_oferta)
#
#         g.save