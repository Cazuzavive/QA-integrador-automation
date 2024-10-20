def es_primo(n):
    # Los números menores que 2 no son primos
    if n < 2:
        return False
    # Verificar si n es divisible por algún número entre 2 y la raíz cuadrada de n
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


numero = int(input("Ingresa un número: "))

# Verificacion
if es_primo(numero):
    print(f"{numero} es un número primo.")
else:
    print(f"{numero} no es un número primo.")
