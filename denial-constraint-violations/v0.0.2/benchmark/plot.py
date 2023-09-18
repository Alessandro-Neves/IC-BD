import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import pandas

df = pandas.read_csv('results_many_detectors.csv')

collumns = df.columns.tolist()

dc1_times = df.iloc[0].values.astype(float)
dc2_times = df.iloc[1].values.astype(float)
dc3_times = df.iloc[2].values.astype(float)
dc4_times = df.iloc[3].values.astype(float)

x_indexes = ['1k', '5k', '10k', '20k', '40k']

plt.plot(x_indexes, dc1_times, marker='o', label='Pandas')
plt.plot(x_indexes, dc2_times, marker='o', label='Polars')
plt.plot(x_indexes, dc3_times, marker='o', label='DuckDB')
plt.plot(x_indexes, dc4_times, marker='o', label='DuckDB DISTINCT')
plt.title('1 DC, Many DCDetectors')
plt.xlabel('Datasets')
plt.ylabel('Time exec (s)')
plt.grid(True)
plt.legend()  # Mostra a legenda

# Salvar o gráfico como uma imagem na pasta
plt.savefig('1-dc-many-detectors-benchmark.png')

# Limpar o buffer de plots (se você deseja criar mais gráficos)
plt.clf()