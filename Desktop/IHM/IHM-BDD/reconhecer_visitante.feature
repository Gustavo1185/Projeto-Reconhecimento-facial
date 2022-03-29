Feature: reconhecer um aluno pela foto

Scenario: Um aluno chega a escola e deve ser reconhecido por uma camera
Given o ambiente de reconhecimento seja preparado com sucesso
When a foto faces/elliot1.jpg de um visitante for capturada
Then um aluno deve ser reconhecido

Scenario: Um aluno chega a escola e nao deve ser reconhecido por uma camera
Given o ambiente de reconhecimento seja preparado com sucesso
When a foto faces/angela1.jpeg de um visitante for capturada
Then um aluno nao deve ser reconhecido