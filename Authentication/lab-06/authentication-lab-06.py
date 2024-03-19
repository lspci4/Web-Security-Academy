# Nombre del archivo que contiene las contraseñas
file_name = '/home/lspci4/Web-Security-Academy/Authentication/lab-06/passwords.txt'

# Leer las contraseñas del archivo
with open(file_name, 'r') as file:
    passwords = file.read().splitlines()  # Crea una lista de contraseñas, una por línea

# Lista para guardar el resultado
result = []

# Iterar sobre la lista de contraseñas, dos por vez
for i in range(0, len(passwords), 2):
    result.extend(passwords[i:i+1])  # Añade las dos siguientes contraseñas
    result.append("peter")  # Añade "peter" después de cada par de contraseñas

# Convertir la lista de resultados en una cadena de texto, uniendo elementos con saltos de línea
result_text = '\n'.join(result)

# Nombre del nuevo archivo para guardar el resultado
new_file_name = '/home/lspci4/Web-Security-Academy/Authentication/lab-06/result.txt'

# Guardar el resultado en el nuevo archivo
with open(new_file_name, 'w') as new_file:
    new_file.write(result_text)
    print(result)



