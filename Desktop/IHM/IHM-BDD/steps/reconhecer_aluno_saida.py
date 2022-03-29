from behave  import  given, when, then
from escola import *

@given("o ambiente de reconhecimento foi preparado com sucesso")
def given_ambiente_reconhecimento_preparado(context):
    context.configuracao, context.alunos_reconhecidos, context.aluno_em_sala, context.aluno_em_refeitorio, context.aluno_saida,context.gerador_dados_falsos = preparar()
    
    context.aluno_reconhecidos = {}
    assert context.configuracao!= None

@when("a foto {foto_visitante} de um aluno for capturada")    
def when_foto_visitante_capturada(context, foto_visitante):
    visitante = simular_visita(foto_visitante)
    context.reconhecido, context.aluno = alunos_saida(visitante, context.alunos_reconhecidos,context.configuracao, context.gerador_dados_falsos)
    
    assert True     

@then("um aluno deve ser reconhecido saindo da escola")
def then_aluno_reconhecido(context):
    id_visitante = secrets.token_hex(nbytes=16).upper()
    context.aluno_reconhecidos[id_visitante]= context.aluno
    
    assert context.reconhecido is True  