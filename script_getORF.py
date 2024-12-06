#!/usr/bin/env python3

# P2 Parte 2  
# Nome: Mark Kevin Bilsland Marchean
# N°USP:12532865

# Exercicio 2

import sys

def analisar_fasta(caminho):
    """Seccionar elementos do arquivo multifasta para um dicionáio: {cabecalho: sequencia}."""
    sequencias = {}
    cabecalho = None
    sequencia = []

    with open(caminho, 'r') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if linha.startswith(">"):
                if cabecalho:
                    sequencias[cabecalho] = ''.join(sequencia)
                cabecalho = linha[1:]
                sequencia = []
            else:
                sequencia.append(linha)
        if cabecalho:
            sequencias[cabecalho] = ''.join(sequencia)

    return sequencias

def fazer_complementar(sequencia):
    """Obtenha o complemento reverso de uma sequência de DNA."""
    
    complemento = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    # Substituir cada base pelo seu complemento
    complementar = ''.join(complemento[base] for base in sequencia)
    # Retornar o complemento reverso
    return complementar[::-1]

def encontrar_orf_mais_longo(sequencia, tabela_de_codons, codon_de_inicio='ATG', codons_de_terminio={'TAA', 'TAG', 'TGA'}):
    """Identifique o maior ORF em uma sequência em todas as 6 fases de leitura."""
    orf_mais_comprido = {"orf": "", "peptidio": "", "frame": 0, "start": 0, "end": 0}
    fitas = [sequencia, fazer_complementar(sequencia)]

    for strand_index, fita in enumerate(fitas):
        for frame in range(3):
            orf_inicio = None
            orf_sequencia = []
            for i in range(frame, len(fita) - 2, 3):
                codon = fita[i:i + 3]
                if codon == codon_de_inicio:
                    orf_inicio = i
                    orf_sequencia = [codon]
                elif orf_inicio is not None:
                    orf_sequencia.append(codon)
                    if codon in codons_de_terminio:
                        orf_length = len(orf_sequencia) * 3
                        if orf_length > len(orf_mais_comprido["orf"]):
                            orf_mais_comprido = {
                                "orf": ''.join(orf_sequencia),
                                "peptidio": ''.join([tabela_de_codons[c] for c in orf_sequencia if c in tabela_de_codons]),
                                "frame": frame + 1 if strand_index == 0 else frame + 4,
                                "start": orf_inicio + 1,
                                "end": i + 3
                            }
                        orf_inicio = None
                        orf_sequencia = []
    return orf_mais_comprido

def escreva_output(nome_do_arquivo, dados):
    """Escreva os dados em um arquivo fasta."""
    with open(nome_do_arquivo, 'w') as arquivo:
        for cabecalho, sequencia in dados:
            arquivo.write(f">{cabecalho}\n{sequencia}\n")

def main():
    if len(sys.argv) != 2:
        print("Uso: python script_getORF.py <input_multifasta>")
        sys.exit(1)

    input_file = sys.argv[1]
    tabela_de_codons = {
        'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L', 'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
        'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M', 'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
        'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S', 'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
        'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T', 'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
        'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*', 'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K', 'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
        'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W', 'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
        'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R', 'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
    }

    sequencias = analisar_fasta(input_file)
    orf_fasta = []
    peptidio_fasta = []

    for cabecalho, sequencia in sequencias.items():
        orf_mais_comprido = encontrar_orf_mais_longo(sequencia, tabela_de_codons)
        novo_cabecalho = f"{cabecalho}_frame{orf_mais_comprido['frame']}_{orf_mais_comprido['start']}_{orf_mais_comprido['end']}"
        orf_fasta.append((novo_cabecalho, orf_mais_comprido["orf"]))
        peptidio_fasta.append((novo_cabecalho, orf_mais_comprido["peptidio"]))

    escreva_output("ORF.fna", orf_fasta)
    escreva_output("ORF.faa", peptidio_fasta)
    print("Processamento concluído. Saída escrita em ORF.fna e ORF.faa.")

if __name__ == "__main__":
    main()
