import face_recognition
import secrets
import random
import faker
import simpy
import json
from datetime import datetime

FOTOS_VISITANTES = [
    "faces/angela1.jpeg",
    "faces/tyrell1.jpeg",
    "faces/price1.jpg",

    "faces/darlene1.jpg",
    "faces/darlene2.jpg",
    "faces/darlene3.jpg",

    "faces/elliot1.jpg",
    "faces/elliot2.jpg",
    "faces/elliot3.jpg"
]

fotos_sala = ["sala/tonho2.jpg",
             "sala/tonho3.jpg",
             "sala/tonho4.jpg",
             
             "sala/loki1.jpg",
             "sala/loki2.jpg",
             "sala/loki3.jpg",
             "sala/loki4.jpg"
             ]



ARQUIVO_CONFIGURACAO = "configuracao.json"
PROBABILIDADE_A= 6
PROBABILIDADE_B= 36
PROBABILIDADE_C = 2
PROBABILIDADE_D= 9
PROBABILIDADE_E= 1



PROBABILIDADE_DE_ESTAR_EM_SALA = 50
PROBABILIDADE_DE_NAO_ESTAR_EM_SALA = 50
TEMPO_ENTRE_VISITANTES = 150
TEMPO_RECONHECIMENTO_SALA = 60
TEMPO_RECONHECIMENTO_REFEITORIO = 60
TEMPO_LIBERACAO_PACIENTE = 90
TEMPO_LIBERACAO_UTI = 500

def preparar():
    global configuracao
    
    configuracao = None
    with open(ARQUIVO_CONFIGURACAO, "r") as arquivo_configuracao:
        configuracao = json.load(arquivo_configuracao)
        if configuracao:
            print("configuracao carregada. versão da simulação:", configuracao["versao"])
            
    global alunos_reconhecidos
    alunos_reconhecidos = {}

    global aluno_em_sala
    aluno_em_sala = {}

    global aluno_em_refeitorio 
    aluno_em_refeitorio = {}
    
    global aluno_saida 
    aluno_saida = {}
    
    

    global gerador_dados_falsos
    gerador_dados_falsos = faker.Faker(locale="pt_BR")
    
    
def simular_visita():
    visitante = {
        "foto": random.choice(FOTOS_VISITANTES),
        "identificacao": None
    }

    return visitante


def reconhecer_aluno(visitante):
    global configuracao
    global gerador_dados_falsos

    print("iniciando reconhecimento do aluno...")
    foto_visitante = face_recognition.load_image_file(visitante["foto"])
    encoding_foto_visitante = face_recognition.face_encodings(foto_visitante)[0]

    reconhecido = False
    for identificacao in configuracao["identificacao"]:
        fotos_banco = identificacao["fotos"]
        total_reconhecimentos = 0

        for foto in fotos_banco:
            foto_banco = face_recognition.load_image_file(foto)
            encoding_foto_banco = face_recognition.face_encodings(foto_banco)[0]

            foto_reconhecida = face_recognition.compare_faces([encoding_foto_visitante], encoding_foto_banco)[0]
            if foto_reconhecida:
                total_reconhecimentos += 1

        if total_reconhecimentos/len(fotos_banco) > 0.7:
            reconhecido = True

            visitante["identificacao"] = {}
            visitante["identificacao"]["nome"] = gerador_dados_falsos.name()
            visitante["identificacao"]["idade"] = random.randint(10, 18)
            visitante["identificacao"]["turma"] = random.choice(["A", "B", "C", "D", "E",])
            visitante["identificacao"]["ano"] = random.choice(["1", "2", "3", "4", "5","6","7","8"])
            visitante["identificacao"]["turno"] = random.choice(["Manha", "Tarde", "Integral"])
            visitante["identificacao"]["valor"] = random.choice(["R$ 3,00", "R$ 4,00", "R$ 5,00"])
            visitante["identificacao"]["produto"] = random.choice(["Coxinha", "Empada", "Pastel","Pizza"])
            

    return reconhecido, visitante

def imprimir_identificacao(aluno):
    print("nome:", aluno["identificacao"]["nome"])
    print("idade:", aluno["identificacao"]["idade"])
    print("turma:", aluno["identificacao"]["turma"])
    print("ano do aluno:", aluno["identificacao"]["ano"])
    print("turno:", aluno["identificacao"]["turno"])
    
def imprimir_comprovante(aluno):
    print("nome:", aluno["identificacao"]["nome"])
    print("idade:", aluno["identificacao"]["idade"])
    print("turma:", aluno["identificacao"]["turma"])
    print("ano do aluno:", aluno["identificacao"]["ano"])
    print("turno:", aluno["identificacao"]["turno"])
    print("valor:", aluno["identificacao"]["valor"])
    print("produto:", aluno["identificacao"]["produto"])
    
def reconhecer_visitante(env):
    global alunos_reconhecidos
    
    while True:
        print("reconhecendo um aluno em ciclo/tempo", env.now)

        visitante = simular_visita()
        reconhecido, aluno = reconhecer_aluno(visitante)
        if reconhecido:
            id_aluno = secrets.token_hex(nbytes=16).upper()
            alunos_reconhecidos[id_aluno] = aluno

            print("um aluno foi reconhecido entrando na escola, imprimindo o identificacao...")
            imprimir_identificacao(aluno)
            data_e_hora_atuais = datetime.now()
            data_e_hora_em_texto = data_e_hora_atuais.strftime("%d/%m/%Y %H:%M")
            print(data_e_hora_em_texto)
            
        else:
            print("não foi reconhecido o aluno")
            
        yield env.timeout(TEMPO_ENTRE_VISITANTES)
        
        
def identificar_aluno_sala(env):
    global alunos_reconhecidos
    global aluno_em_sala
    
    while True:
        if len(alunos_reconhecidos):
            print("verificando situacao do aluno em ciclo/tempo", env.now)

            total_aluno_em_sala = 0
            for id_aluno, aluno in list(alunos_reconhecidos.items()):
                
                foto_original = "sala/loki1.jpg"
                configurar_reconhecedor(foto_original)
                foto = random.choice(fotos_sala)
                aluno_sala_reconhecido = comparar_com_original(foto)    
                
                if aluno_sala_reconhecido == [True]:
                    aluno_em_sala[id_aluno] = aluno
                    alunos_reconhecidos.pop(id_aluno)

                    print("aluno", aluno["identificacao"]["nome"], "esta em sala de aula")

                    total_aluno_em_sala += 1
                    
                if aluno_sala_reconhecido == [False]:
                    aluno_em_sala[id_aluno] = aluno
                    alunos_reconhecidos.pop(id_aluno)

                    print("aluno", aluno["identificacao"]["nome"], "não esta em sala de aula")   
                
            timeout = 1
            if total_aluno_em_sala > 0:
                timeout = total_aluno_em_sala * TEMPO_RECONHECIMENTO_SALA

            yield env.timeout(timeout)
        else:
            yield env.timeout(1)
 
 
def configurar_reconhecedor(foto_original):
    global encoding_foto_original
    
    foto = face_recognition.load_image_file(foto_original)
    encoding_foto_original = face_recognition.face_encodings(foto)[0]

def comparar_com_original(foto):
    global encoding_foto_original
    
    resultado = None
    
    try:
        nova_foto = face_recognition.load_image_file(foto)
        enconding_nova_foto = face_recognition.face_encodings(nova_foto)[0]
        
        resultado = face_recognition.compare_faces([encoding_foto_original], enconding_nova_foto)
    except:
        pass    
    
    return resultado
 
 
def compras_aluno_refeitorio(env):
    global alunos_reconhecidos
    
    while True:
        print("reconhecendo um aluno em ciclo/tempo", env.now)

        visitante = simular_visita()
        reconhecido, aluno = reconhecer_aluno(visitante)
        if reconhecido:
            id_aluno = secrets.token_hex(nbytes=16).upper()
            alunos_reconhecidos[id_aluno] = aluno

            print("um aluno foi reconhecido no refeitorio, imprimindo comprovante...")
            imprimir_comprovante(aluno)
            
        else:
            print("o aluno não possui conta cadastrada no refeitorio")
            
        yield env.timeout(TEMPO_ENTRE_VISITANTES)
        
def alunos_saida(env):
    global alunos_reconhecidos
    
    while True:
        print("reconhecendo um aluno em ciclo/tempo", env.now)

        visitante = simular_visita()
        reconhecido, aluno = reconhecer_aluno(visitante)
        if reconhecido:
            id_aluno = secrets.token_hex(nbytes=16).upper()
            alunos_reconhecidos[id_aluno] = aluno

            print("um aluno foi reconhecido saindo da escola, imprimindo descricao...")
            imprimir_identificacao(aluno)
            data_e_hora_atuais = datetime.now()
            data_e_hora_em_texto = data_e_hora_atuais.strftime("%d/%m/%Y %H:%M")
            print(data_e_hora_em_texto)
            

            
        yield env.timeout(TEMPO_ENTRE_VISITANTES)
 
        

if __name__ == "__main__":
    preparar()

    env = simpy.Environment()
    env.process(reconhecer_visitante(env))
    env.process(identificar_aluno_sala(env))
    env.process(compras_aluno_refeitorio(env))
    env.process(alunos_saida(env))
    env.run(until=1000)
    