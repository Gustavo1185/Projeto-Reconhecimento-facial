Feature: verificando se o aluno saiu da escola

Scenario: Um aluno sai da escola e deve ser reconhecido por uma camera
Given o ambiente de reconhecimento foi preparado com sucesso
When a foto faces/elliot1.jpg de um aluno for capturada
Then um aluno deve ser reconhecido saindo da escola