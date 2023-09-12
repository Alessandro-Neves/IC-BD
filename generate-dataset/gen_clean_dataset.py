import pandas as pd
import random

# Função para gerar o valor aleatório do bônus
def generate_bonus():
    return round(random.uniform(100.00, 7000.00), 2)
  
# Função para aplicar a função x à tupla e retornar True ou False
def apply_x_function(tupla, df):
  
  # t1.salary > t2.salary, t1.hiring_year > t2.hiring_year
  p_cond_a = (tupla['salary'] > df['salary']) & (tupla['hiring_year'] > df['hiring_year'])
  
  if p_cond_a.any():
    return False
  
    # Substitua esta lógica pela sua função x
    # Neste exemplo, retornaremos True para todas as tuplas
  return True

# Leitura dos arquivos com nomes e sobrenomes
with open('names.txt', 'r') as nomes_file:
    nomes = [line.strip() for line in nomes_file]

with open('surnames.txt', 'r') as sobrenomes_file:
    sobrenomes = [line.strip() for line in sobrenomes_file]

# Número de tuplas desejado (L)
num_tuples = 20000

# Inicialização do DataFrame
data = {'id': [], 'name': [], 'salary': [], 'bonus': [], 'hiring_year': [], 'dismissing_year': []}

# Geração das tuplas
id_counter = 0
while len(data['id']) < num_tuples:
    print(f"gen {id_counter}")
    name = f"{random.choice(nomes)}-{random.choice(sobrenomes)}"
    salary = round(random.uniform(1320.00, 37800.80), 2)
    hiring_year = random.randint(1990, 2023)
    dismissing_year = random.randint(hiring_year, 2023)
    bonus = generate_bonus()

    tupla = {'id': id_counter, 'name': name, 'salary': salary, 'bonus': bonus, 'hiring_year': hiring_year, 'dismissing_year': dismissing_year}

    # t1.salary < t1.bonus
    cond_a = tupla['salary'] < tupla['bonus']
    
    # t1.hiring_year > t1.dismissing_year
    cond_b = tupla['hiring_year'] > tupla['dismissing_year']
    
    if cond_a or cond_b:
      continue
  
    # Aplicar a função x à tupla
    if apply_x_function(tupla, pd.DataFrame(data)):
        # Se a função x retornar True, adicione a tupla ao DataFrame
        for key, value in tupla.items():
            data[key].append(value)
        id_counter += 1

# Criar o DataFrame
df = pd.DataFrame(data)

# Salvar o DataFrame em um arquivo CSV
df.to_csv('dataset.csv', index=False)