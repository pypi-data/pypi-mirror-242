import numpy as np


# definimos una función
def saludar():
    print("Hola te saludo desde sub paquete saludos. ¡Hola!, Hello!, Bonjour!".title())


# Definimos una clase para instancias
class Saludo:
    def __init__(self):
        print("Hola te saludo desde clase Saludo. ¡Hola!, Hello!, Bonjour! ".title())


# funcion externa

def generar_array(numeros):
    return np.arange(numeros)


if __name__ == "__main__":
    print(generar_array(5))

"""
Nos dará un resultado [0 1 2 3 4]
Se utiliza la función arange de NumPy para generar el array. La función arange en el módulo NumPy de Python se 
utiliza para crear un array que contiene una secuencia de números espaciados uniformemente. 

En Python, hay dos estructuras de datos comunes para almacenar secuencias de elementos: listas y arrays NumPy. 
Aquí hay algunas diferencias clave entre ellas:

Listas de Python:
Flexibilidad de Tipo:

Las listas en Python pueden contener elementos de diferentes tipos. Puedes tener enteros, cadenas, objetos, etc., 
en la misma lista.
Operaciones Básicas:

Las listas ofrecen una variedad de operaciones básicas como añadir, quitar y modificar elementos. Las operaciones 
básicas a menudo implican iterar a través de la lista.
Sintaxis Simple:

La sintaxis para trabajar con listas es simple y directa. Se definen utilizando corchetes [].
Arrays NumPy:
Homogeneidad de Tipo:

Los arrays NumPy contienen elementos del mismo tipo. Esto permite operaciones más eficientes y evita la necesidad de 
comprobaciones de tipo en las operaciones.
Operaciones Vectorizadas:

Los arrays NumPy admiten operaciones vectorizadas. Las operaciones se aplican a todos los elementos del array de una 
vez, sin necesidad de bucles explícitos. Esto mejora el rendimiento.
Funcionalidades Numéricas:

NumPy proporciona una amplia gama de funciones y métodos específicos para operaciones numéricas, algebraicas, 
estadísticas, etc. Está optimizado para el cálculo numérico y es ampliamente utilizado en ciencia de datos y 
computación científica.
Eficiencia en Memoria:

Los arrays NumPy son más eficientes en términos de uso de memoria para grandes conjuntos de datos numéricos, ya 
que almacenan datos de manera más compacta y utilizan memoria de manera más eficiente.
En resumen, las listas de Python son versátiles y fáciles de usar, mientras que los arrays NumPy están diseñados 
para operaciones numéricas eficientes y son más eficientes en términos de rendimiento y uso de memoria cuando 
trabajas con grandes conjuntos de datos numéricos. La elección entre ellas dependerá de tus necesidades específicas 
y del tipo de operaciones que planees realizar.

"""