#!/usr/bin/env python3

# Prova 2 Parte 2 Exercicio 4
# Nome: Mark Kevin Bilsland Marchean
# N°USP:12532865

def calcular_media_disciplina():
    total = 0
    contador = 0

    while contador < 10:
        print("Digite uma nota (de 0 a 10):")
        nota = input()
        try:
            nota = float(nota)
            if nota >= 0 and nota <= 10:
                total = total + nota
                contador = contador + 1
            else:
                print("Nota inválida, tente de novo.")
        except:
            print("Erro: Digite um número válido.")

    media = total / 10
    print("Média final:", round(media, 2))

calcular_media_disciplina()
