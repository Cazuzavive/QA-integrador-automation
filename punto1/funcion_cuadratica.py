import math

def resolver_ecuacion_cuadratica(a, b, c):
    # Calculamos 
    discriminante = b**2 - 4*a*c
    
    # cmath.sqrt para raíces 
    raiz_discriminante = math.sqrt(discriminante)
    
    # Calculamos las dos soluciones
    x1 = (-b + raiz_discriminante) / (2 * a)
    x2 = (-b - raiz_discriminante) / (2 * a)
    
    return x1, x2

# Ejemplo
a = 1
b = -3
c = 2
raices = resolver_ecuacion_cuadratica(a, b, c)
print(f"Las raíces de la ecuación son: {raices}")
