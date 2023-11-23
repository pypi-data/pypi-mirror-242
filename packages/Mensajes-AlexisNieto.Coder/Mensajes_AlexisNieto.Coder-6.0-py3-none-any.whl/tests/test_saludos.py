import unittest
import numpy as np
# módulo de testing es una parte separada de NumPy y no se incluye automáticamente al importar el paquete principal
from numpy import testing
from mensajes2.saludos.saludos_mod_externo import generar_array


# Generar los test
class PruebasSaludos(unittest.TestCase):
    # PRIMER TEST
    # noinspection PyMethodMayBeStatic
    def test_generar_array(self):
        # Utilizaremos el test de numpy en vez de self.assertEquals() usamos el  testing.assert_array_equal
        # una función de aserción proporcionada por el módulo de testing de NumPy (numpy.testing).
        # Su propósito principal es verificar si dos arrays de NumPy son iguales
        np.testing.assert_array_equal(
            # 01 elementos que se probaran
            np.array([0, 1, 2, 3, 4, 5]),
            # 02 elementos que se esperan que sean idénticos a 01
            generar_array(6)
        )
