Feature: reconhecer um aluno ao entrar na sala

Scenario: Um aluno chega na sala e deve ser reconhecido por uma camera
Given o ambiente de reconhecimento estara preparado com sucesso
When a foto faces/elliot1.jpg de um aluno na sala for capturada
Then um aluno deve ser reconhecido entrando na sala