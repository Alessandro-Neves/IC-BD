import pandas as pd
import random

# Função para gerar o valor aleatório do bônus
def generate_bonus():
    return round(random.uniform(100.00, 7000.00), 2)
  
# Função para aplicar a função x à tupla e retornar True ou False
def apply_x_function(tupla, df):
  
  # t1.salary > t2.salary, t1.hiring_year > t2.hiring_year
  p_cond_a = (tupla['salary'] > df['salary']) & (tupla['hiring_year'] > df['hiring_year']) & (tupla['occupation'] == df['occupation'])
  p_cond_a_inv = (tupla['salary'] < df['salary']) & (tupla['hiring_year'] < df['hiring_year']) & (tupla['occupation'] == df['occupation'])
  
  if not df[p_cond_a].empty or not df[p_cond_a_inv].empty:
    return False
  
  return True

# Leitura dos arquivos com nomes e sobrenomes
with open('names.txt', 'r') as nomes_file:
  nomes = [line.strip() for line in nomes_file]

with open('surnames.txt', 'r') as sobrenomes_file:
  sobrenomes = [line.strip() for line in sobrenomes_file]
    
with open('occupations.txt', 'r') as occupations_file:
  occupations = [line.strip() for line in occupations_file]

num_tuples = 25000

df = pd.read_csv('dataset.csv')

id_counter = df.shape[0]
while id_counter < num_tuples:
  print(f"gen {id_counter}")
  id = id_counter
  name = f"{random.choice(nomes)}-{random.choice(sobrenomes)}"
  salary = round(random.uniform(1320.00, 37800.80), 2)
  hiring_year = random.randint(1980, 2023)
  dismissing_year = random.randint(hiring_year, 2023)
  bonus = generate_bonus()
  occupation = random.choice(occupations)

  tupla = {
    'id': id, 
    'name': name, 
    'salary': salary, 
    'bonus': bonus, 
    'hiring_year': hiring_year, 
    'dismissing_year': dismissing_year,
    'occupation': occupation
  }

  # t1.salary < t1.bonus
  cond_a = tupla['salary'] < tupla['bonus']
  
  # t1.hiring_year > t1.dismissing_year
  cond_b = tupla['hiring_year'] > tupla['dismissing_year']
  
  if cond_a or cond_b:
    continue

  if apply_x_function(tupla, df):
      
      df.loc[len(df)] = [id, name, salary, bonus, hiring_year, dismissing_year, occupation]
      id_counter += 1

  if (id_counter % 100) == 0:
    df.to_csv('dataset.csv', index=False)
