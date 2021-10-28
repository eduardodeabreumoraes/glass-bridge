import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from multiprocessing import Pool
from multiprocessing import cpu_count
number_of_threads = cpu_count()
from itertools import repeat

#Função que gera uma lista que representa (D = direita; E = esquerda) em um caminho com 'n' placas
def path_creator(n):
    path = random.choices(['D', 'E'], k=n)
    return path

#Função que cria uma lista de jogadores numerados de 1 a 'n'
def players_creator(n):
    players = list(range(1, n+1))
    return players

#Função que representa uma partida e retorna o primeiro jogador a vencer.
def first_winner(params):
    number_of_tiles, number_of_players = params
    safe_tiles = path_creator(number_of_tiles)
    players = players_creator(number_of_players)
    for player in players:
        if len(safe_tiles) == 0:
            return player
        player_strategy = path_creator(len(safe_tiles))
        for i in player_strategy:
            if i == safe_tiles[0]:
                del safe_tiles[0]
                if len(safe_tiles) == 0:
                    return player
            else:
                del safe_tiles[0]
                break #hehehe
    return 'Ninguém'

#Roda 'n' simulações
n = 300000000
number_of_tiles = 18
number_of_players = 16
if __name__ == '__main__':
    with Pool(processes=number_of_threads) as p:
        resultados = p.map(first_winner, repeat((number_of_tiles, number_of_players),n))
        p.close()

#Remove os resultados "Ninguém"
resultados = [i for i in resultados if i != 'Ninguém']

#Obtém o número de vezes que cada jogador foi o primeiro vencedor
first_victory_count = np.unique(resultados, return_counts=True)
players = first_victory_count[0]
number_of_victories = first_victory_count[1]

#Calcula a probabilidade de cada jogador em ser o primeiro a vencer
probabilities = number_of_victories / n

#Transforma o array de probabilidades em uma série do pandas
probabilities = pd.Series(probabilities, players)

#Gera o gráfico da probabilidade do jogador ser o primeiro a vencer
ax = probabilities.plot.bar(figsize=(16,9))
ax.axes.set_title("Probabilidade de cada jogador ser o primeiro a vencer",fontsize=14)
ax.bar_label(ax.containers[0])
plt.savefig("Probabilidade de cada jogador ser o primeiro a vencer", bbox_inches='tight')
plt.close()

#Calcula a probabilidade de cada jogador simplesmente vencer
cum_probabilities = probabilities.cumsum()

#Gera o gráfico da probabilidade do jogador vencer
ax = cum_probabilities.plot.bar(figsize=(16,9))
ax.axes.set_title("Probabilidade de cada jogador vencer",fontsize=14)
ax.bar_label(ax.containers[0])
plt.savefig("Probabilidade de cada jogador vencer", bbox_inches='tight')
plt.close()


