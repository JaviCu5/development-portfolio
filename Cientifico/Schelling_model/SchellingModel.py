import numpy as np
import random as rd
import os
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

lateral_size = 50
total_cells = lateral_size*lateral_size

occupancy = 0.8

satisfaction = 0.3

A_ratio = 0.5 #We will use -1 for this individuals
A_value = -1
A_individuals = round(total_cells*occupancy*A_ratio)

B_ratio = 1.-A_ratio #We will use 1 for this individuals
B_value = 1
B_individuals = round(total_cells*occupancy)-A_individuals
# We Will use 0 for blank places

'''
def local_satisfaction_segregation(matrix, row, col):
      rows, cols = len(matrix), len(matrix[0])
      total = []
      
      for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                  if (0 <= i < rows and 0 <= j < cols) and (i != row or j != col):
                  
                        total.append(matrix[i][j])
      return local_satisfaction, local_segregation
'''

def rand_initial_configuration_square_lattice(lateral_size, A_individuals, B_individuals):
      initial_conf = np.zeros((lateral_size,lateral_size))
      indexes = [(i, j) for i in range(lateral_size) for j in range(lateral_size)]
      indexes = np.array(indexes)
      
      np.random.shuffle(indexes)
      
      A_indexes = indexes[:A_individuals]
      B_indexes = indexes[A_individuals:A_individuals+B_individuals]
      void_indexes = indexes[A_individuals+B_individuals:]
      
      for dupla_A in A_indexes:
            initial_conf[dupla_A[0], dupla_A[1]] = '-1'
      
      for dupla_B in B_indexes:
            initial_conf[dupla_B[0], dupla_B[1]] = '1'
      
      return initial_conf, void_indexes

def cmap_creator(matrix, fig_name, A_value, B_value):
      if not os.path.exists('images'):
            os.mkdir('images')
      cmap = plt.get_cmap('bwr')

      # Definir los límites de color según tu rango (-1 a 1)
      vmin, vmax = A_value, B_value

      # Mostrar la matriz con el colormap y los límites
      plt.imshow(matrix, cmap=cmap, vmin=vmin, vmax=vmax, origin='lower')
      plt.savefig('images/'+fig_name+'.png')

initial_conf, void_indexes = rand_initial_configuration_square_lattice(lateral_size, A_individuals, B_individuals)
cmap_creator(initial_conf, 'rand_conf', A_value, B_value)

# Example of use:
matrix = np.zeros((lateral_size,lateral_size))
row = 2
column = 2

neighbors = type(matrix)#sum_eight_neighbors(matrix, row, column)
print(neighbors)
