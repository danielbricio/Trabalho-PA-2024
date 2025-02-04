from gera_array import GeraArray
from quick_sort import QuickSort
from heap_sort import HeapSort
from merge_sort import MergeSort
import pandas as pd
import matplotlib.pyplot as plt

def grafico_array(A, tamanho_array, tipo_array, estado):
    plt.figure(figsize=(10, 6))
    plt.plot(A, label=f"{estado} da Ordenação", color="blue")
    plt.title(f"Array {estado} da Ordenação - {tipo_array} ({tamanho_array})")
    plt.xlabel("Índice")
    plt.ylabel("Valor")
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"/home/rubens/Trabalho-Algoritmo-2024/algoritmos_eficientes/resultados/graficos/{tamanho_array}/array_{estado}_{tipo_array}.jpg")
    plt.close()

if __name__ == "__main__":
    algoritmos = [QuickSort(), HeapSort(), MergeSort()]
    tamanhos_array = [10,100,1000,10000,100000,1000000]
    tipos_array = ["ordenado_cresc", "ordenado_descr", "quase_ordenado", "aleatorio"]
    array = GeraArray()

    # DataFrame para consolidar todos os resultados
    todos_resultados = []

    for tamanho_array in tamanhos_array:

        for tipo_array in tipos_array:
            resultados = []
            metodo_array = getattr(array, tipo_array)
            A = metodo_array(tamanho_array)
            grafico_array(A, tamanho_array, tipo_array, 'antes')
            
            for algoritmo in algoritmos:
                
                algoritmo.sort(A)
                grafico_array(A, tamanho_array, tipo_array, 'depois')
                resultado = algoritmo.resultados()
                resultado.update({
                    "algoritmo": type(algoritmo).__name__,
                    "tamanho_array": tamanho_array,
                    "tipo_array": tipo_array
                })
                resultados.append(resultado)

            # Adiciona os resultados ao DataFrame consolidado
            todos_resultados.extend(resultados)

            # Cria um DataFrame específico para a combinação atual
            df = pd.DataFrame(resultados)

            # Gera o gráfico para a combinação atual
            
            plt.figure(figsize=(10, 6))
            bar_width = 0.25
            x = range(len(df['algoritmo']))

            for i, metrica in enumerate(["comparacoes", "atribuicoes", "tempo_execucao"]):
                plt.bar(
                    [p + bar_width * i for p in x],
                    df[metrica],
                    bar_width,
                    label=metrica
                )

            plt.title(f"Resultados para {tipo_array} com tamanho {tamanho_array}")
            plt.xlabel("Algoritmo")
            plt.ylabel("Valores")
            plt.xticks([p + bar_width for p in x], df['algoritmo'])
            plt.legend()
            plt.grid(axis="y")
            plt.tight_layout()
            plt.savefig(f"/home/rubens/Trabalho-Algoritmo-2024/algoritmos_eficientes/resultados/graficos/{tamanho_array}/grafico_{tipo_array}.jpg")
            plt.close()

    # Salva o DataFrame consolidado como CSV
    df_consolidado = pd.DataFrame(todos_resultados)
    df_consolidado.to_csv("/home/rubens/Trabalho-Algoritmo-2024/algoritmos_eficientes/resultados/dataframes/todos_resultados.csv", index=False)
