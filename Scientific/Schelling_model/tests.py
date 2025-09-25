import numpy as np

mi_array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
elemento = np.array([4, 5, 6])

# Encuentra las ubicaciones donde los subarrays coinciden con el elemento
ubicaciones = np.where(np.all(mi_array == elemento, axis=1))

# Si se encontraron ubicaciones
if len(ubicaciones[0]) > 0:
      # Elimina los subarrays completos
      mi_array = np.delete(mi_array, ubicaciones[0], axis=0)

print(mi_array, ubicaciones)