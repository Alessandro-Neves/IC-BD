import random
from faker import Faker


# Gerar 300 nomes aleatórios
fake = Faker()
names = set()

while len(names) < 300:
    name = fake.first_name().replace(" ", "").strip()
    if name.isalpha():
        names.add(name)

with open('names.txt', 'w') as file:
    file.write('\n'.join(names))
    
    

# Gerar 100 sobrenomes aleatórios
fake = Faker()
surnames = set()

while len(surnames) < 100:
    surname = fake.last_name().replace(" ", "").strip()
    if surname.isalpha():
        surnames.add(surname)
        
with open('surnames.txt', 'w') as file:
    file.write('\n'.join(surnames))
    


# Gerar 30 profissões/ocupações aleatórias
# fake = Faker()
# occupations = set()

# while len(occupations) < 30:
#     occupation = fake.job().replace(" ", "-")
#     if occupation.isalpha():
#         occupations.add(occupation)

# with open('occupations.txt', 'w') as file:
#     file.write('\n'.join(occupations))