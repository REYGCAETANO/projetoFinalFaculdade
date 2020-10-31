from django.urls import path

from . import views

app_name = 'gradehoraria'

urlpatterns = [
    path('professores', views.listar_professores, name='listar_professores'),
    path('professores/adicionar/', views.adicionar_professor, name='adicionar_professor'),
    path('professores/editar/<int:id_professor>/', views.editar_professor, name='editar_professor'),
    path('professores/excluir/<int:id_professor>/', views.deleta_professor, name='deleta_professor'),

    path('cursos', views.listar_cursos, name='listar_cursos'),
    path('curso/adicionar/', views.adicionar_curso, name='adicionar_curso'),
    path('curso/editar/<int:id_curso>/', views.editar_curso, name='editar_curso'),
    path('curso/excluir/<int:id_curso>/', views.deleta_curso, name='deleta_curso'),

    path('disciplinas', views.listar_disciplinas, name='listar_disciplinas'),
    path('disciplina/adicionar/', views.adicionar_disciplina, name='adicionar_disciplina'),
    path('disciplina/editar/<int:id_disciplina>/', views.editar_disciplina, name='editar_disciplina'),
    path('disciplina/excluir/<int:id_disciplina>/', views.deleta_disciplina, name='deleta_disciplina'),

    path('turmas', views.listar_turmas, name='listar_turmas'),
    path('turma/adicionar/', views.adicionar_turma, name='adicionar_turma'),
    path('turma/editar/<int:id_turma>/', views.editar_turma, name='editar_turma'),
    path('turma/excluir/<int:id_turma>/', views.deleta_turma, name='deleta_turma'),  path('turmas', views.listar_turmas, name='listar_turmas'),

    path('salas', views.listar_salas, name='listar_salas'),
    path('sala/adicionar/', views.adicionar_sala, name='adicionar_sala'),
    path('sala/editar/<int:id_sala>/', views.editar_sala, name='editar_sala'),
    path('sala/excluir/<int:id_sala>/', views.deleta_sala, name='deleta_sala'),

    path('oferta/adicionar/', views.adicionar_oferta, name='adicionar_oferta'),
    path('oferta/listar/', views.listar_ofertas, name='listar_ofertas'),
    path('oferta/editar/<int:id_oferta>/', views.editar_oferta, name='editar_oferta'),
    path('oferta/excluir/<int:id_oferta>/', views.deleta_oferta, name='deleta_oferta'),

    path('parametros/adicionar/', views.adicionar_parametros, name='adicionar_parametros'),
    path('parametros/listar/', views.listar_parametros, name='listar_parametros'),
    path('parametros/editar/<int:id_parametro>/', views.editar_parametros, name='editar_parametros'),

    path('grade/gerar_grade/', views.gerarGradeHoraria, name='gerarGradeHoraria'),

    #path('', views.gradeHoraria, name='hello_world'),
    #path('', views.index, name='index'),
]
