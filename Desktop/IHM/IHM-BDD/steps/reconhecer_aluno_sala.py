from behave  import  given, when, then
from escola import *

@given("o ambiente de reconhecimento estara preparado com sucesso")
def given_ambiente_reconhecimento_preparado(context):
    context.configuracao, context.alunos_reconhecidos, context.aluno_em_sala, context.aluno_em_refeitorio, context.aluno_saida,context.gerador_dados_falsos = preparar()
    
    context.aluno_reconhecidos = {}
    assert context.configuracao!= None

@when("a foto {foto_original} de um aluno na sala for capturada")    
def when_foto_visitante_capturada(context, foto_original):
        visitante = simular_visita(foto_original)
        context.reconhecido, context.aluno = identificar_aluno_sala(visitante, context.configuracao, context.gerador_dados_falsos,context.alunos_reconhecidos)
    
        assert True     

@then("um aluno deve ser reconhecido entrando na sala")
def then_aluno_reconhecido(context):
    id_visitante = secrets.token_hex(nbytes=16).upper()
    context.aluno_reconhecidos[id_visitante]= context.reconhecido
        
    assert context.reconhecido is True  