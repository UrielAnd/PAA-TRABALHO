# Importando as bibliotecas necessárias
import timeit
from read import Read
import matplotlib.pyplot as plt

# Inicializando a variável global que armazenará o melhor caminho encontrado
melhor_caminho = []

# Função para plotar o melhor caminho encontrado
def plot_best_path(best_path, coordinates):
    # Coordenadas x e y das paradas no melhor caminho
    xs = [coordinates[stop.Stops[0]][0] for stop in best_path]
    ys = [coordinates[stop.Stops[0]][1] for stop in best_path]

    # Criando o gráfico
    plt.figure(figsize=(10, 10))
    plt.plot(xs, ys, marker='o', color='blue')  # Traçando o caminho em azul
    plt.plot(xs[0:2], ys[0:2], marker='o', color='red')  # Primeira parada em vermelho
    for i, stop in enumerate(best_path):  # Adicionando o nome das paradas ao gráfico
        plt.text(xs[i], ys[i], stop.Stops[0])
    plt.show()  # Exibindo o gráfico

# Função para gerar todas as permutações possíveis das paradas
def permutar(Paradas):
    if len(Paradas) == 0:
        return []
    if len(Paradas) == 1:
        return [Paradas]
    l = []
    for i in range(len(Paradas)):
        m = Paradas[i]
        remParadas = Paradas[:i] + Paradas[i+1:]
        for p in permutar(remParadas):
            l.append([m] + p)
    return l

# Função de backtracking para encontrar o melhor caminho
def backtracking(Paradas, QpessoasBus, caminho=[]):
    global melhor_caminho
    # Se a quantidade de pessoas no ônibus exceder 50, retorne e não explore esse ramo
    if QpessoasBus > 50:
        return
    # Se todas as paradas foram visitadas, atualize o melhor caminho
    if len(caminho) == len(Paradas):
        melhor_caminho = caminho
        return melhor_caminho  # Retorna o melhor caminho e sai do backtracking
    # Para cada parada não visitada, explore-a
    for parada in Paradas:
        if parada not in caminho:
            novo_QpessoasBus = QpessoasBus + int(parada.Stops[3])
            if novo_QpessoasBus <= 50:
                # Adicione a parada ao caminho e explore as próximas paradas
                novo_caminho = caminho + [parada]
                print('Caminho atual:', [p.Stops[0] for p in novo_caminho])  # Imprime o caminho atual
                resultado = backtracking(Paradas, novo_QpessoasBus - int(parada.Stops[4]), novo_caminho)
                # Se um caminho válido foi encontrado, retorne e pare de explorar outros ramos
                if resultado is not None:
                    return resultado

# Código principal
if __name__ == "__main__":
  # Lendo as paradas do arquivo Stops.txt
  with open("Stops.txt", "r") as arquivo:
    linhas = arquivo.readlines()
  objetos = [Read(linha) for linha in linhas]

  # Iniciando o cronômetro para medir o tempo de execução do backtracking
  starttime = timeit.default_timer()

  # Executando o algoritmo de backtracking
  backtracking(objetos, 0)

  # Imprimindo o melhor caminho encontrado
  print('Melhor Caminho:', [parada.Stops[0] for parada in melhor_caminho])

  # Parando o cronômetro e imprimindo o tempo de execução do backtracking
  endtime = timeit.default_timer()
  print(f"Tempo de execução do backtracking: {endtime-starttime}")

  # Criando um dicionário com as coordenadas de cada parada
  coordinates = {obj.Stops[0]: (float(obj.Stops[1]), float(obj.Stops[2])) for obj in objetos}

  # Plotando o melhor caminho encontrado
  plot_best_path(melhor_caminho, coordinates)
