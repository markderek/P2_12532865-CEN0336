#!/usr/bin/env python3

# Prova 2 Parte 2 Exercicio 5
# Nome: Mark Kevin Bilsland Marchean
# N°USP:12532865

# Função para contar os nós em uma árvore

def contar_nos(arvore):
    total = 1  # Conta o nó atual
    # Olha cada filho dentro da árvore
    for subarvore in arvore.values():
        # Chama a função de novo para contar os filhos da subárvore
        total = total + contar_nos(subarvore)
    return total  # Retorna o total

# Aqui está a árvore
arvore = {
    "Filo1": {
        "Classe1": {
            "Ordem1": {
                "Familia1": {},
                "Familia2": {}
            },
            "Ordem2": {
                "Familia3": {
                    "Genero3": {},
                    "Genero4": {}
                }
            }
        },
        "Classe2": {
            "Ordem3": {},
            "Ordem4": {
                "Familia4": {},
                "Familia5": {
                    "Genero1": {},
                    "Genero2": {
                        "Especie1": {},
                        "Especie2": {}
                    }
                }
            }
        }
    }
}

# Chamando a função e mostrando o resultado
resultado = contar_nos(arvore)  # Calcula os nós
print("O número total de nós é:", resultado)  # Mostra o resultado
