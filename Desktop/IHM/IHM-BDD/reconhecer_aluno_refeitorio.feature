Feature: reconhecer um aluno no refeitorio pela foto

Scenario: Um aluno chega no refeitorio e deve ser reconhecido por uma camera
Given o ambiente de reconhecimento esta preparado com sucesso
When a foto faces/elliot1.jpg de um aluno no refeitorio for capturada
Then um aluno possui conta cadastrada

Scenario: Um aluno chega no refeitorio e nao deve ser reconhecido por uma camera
Given o ambiente de reconhecimento esta preparado com sucesso
When a foto faces/angela1.jpeg de um aluno no refeitorio for capturada
Then um aluno nao possui conta cadastrada