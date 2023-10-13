import pandas as pd
import random

# Função para gerar o valor aleatório do bônus
def generate_bonus():
    return round(random.uniform(100.00, 7000.00), 2)
  
# Função para aplicar a função x à tupla e retornar True ou False
def apply_x_function(tupla, df):
  # t1.salary > t2.salary, t1.hiring_year > t2.hiring_year
  p_cond_a = (tupla['quantity'] == df['quantity']) & (tupla['tax'] == df['tax']) & (tupla['discount'] < df['discount']) & (tupla['price'] > df['price'])
  p_cond_a_inv = (tupla['quantity'] == df['quantity']) & (tupla['tax'] == df['tax']) & (tupla['discount'] > df['discount']) & (tupla['price'] < df['price'])
  
  if not df[p_cond_a].empty or not df[p_cond_a_inv].empty:
    return False
  
  return True

num_tuples = 1000000

df = pd.read_csv('dataset_lineitem.csv')

id_counter = int(df.shape[0])
while id_counter < num_tuples:
  print(f"gen {id_counter}")
  id = id_counter  
  quantity = random.randint(0, 10000)
  tax = round(random.uniform(0.01, 0.1), 2)
  price = round(random.uniform(1000.00, 50000.00), 2)
  discount = round(random.uniform(0.01, 0.1), 2)
  shipdate = random.randint(15500, 17900)
  receiptdate = random.randint(shipdate, shipdate + 120)

  tupla = {
    'id': id, 
    'quantity': quantity, 
    'tax': tax, 
    'price': price, 
    'discount': discount, 
    'shipdate': shipdate,
    'receiptdate': receiptdate
  }

  if apply_x_function(tupla, df):
      
    df.loc[len(df)] = [str(id), str(quantity), tax, price, discount, str(shipdate), str(receiptdate)]
    id_counter += 1

    if (id_counter % 1000) == 0:
      df.to_csv('dataset_lineitem.csv', index=False)
