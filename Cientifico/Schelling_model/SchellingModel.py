import numpy as np
import random as rd
import os
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image

maxIteration = 10000
## GIF parameters
frame_freq = 50
frame_duration = 200
GIF_images_directory = 'Images'
GIF_name = 'Temporal_evolution'
createGIF = False

lateral_size = 50
occupancy = 0.8
satisfaction = 0.7

total_cells = lateral_size*lateral_size
total_individuals = total_cells*occupancy

A_ratio = 0.5 #We will use -1 for this individuals
A_value = -1
A_individuals = round(total_individuals*A_ratio)

B_ratio = 1.-A_ratio #We will use 1 for this individuals
B_value = 1
B_individuals = int(total_individuals-A_individuals)

# We Will use 0 for blank places
void_value = 0

#Comput of the magnitudes for the initial random system
def initial_matrix_evaluation(lateral_size, satisfaction, system_matrix):
      unhappy_indexes = np.empty((0, 2), dtype=int)
      total_neighbors = 0
      happiness, segregation = 0, 0
      for i in range(lateral_size):
            for j in range(lateral_size):
                  local_value = system_matrix[i,j]
                  if local_value != 0:
                        local_happiness, local_segregation, neigbor_count = local_happiness_segregation(system_matrix, i, j, satisfaction)
                        total_neighbors += neigbor_count
                        if local_happiness == True:
                              happiness += 1
                        else:
                              unhappy_indexes = np.append(unhappy_indexes, np.array([(i,j)]), axis=0)
                        segregation += local_segregation
      return happiness, segregation, total_neighbors, unhappy_indexes

def rand_initial_configuration_square_lattice(lateral_size, A_individuals, B_individuals):
      initial_conf = np.zeros((lateral_size,lateral_size), dtype=int)
      indexes = [(i, j) for i in range(lateral_size) for j in range(lateral_size)]
      indexes = np.array(indexes)
      
      np.random.shuffle(indexes)
      
      A_indexes = indexes[:A_individuals]
      B_indexes = indexes[A_individuals:A_individuals + B_individuals]
      void_indexes = indexes[A_individuals+B_individuals:]
      
      for dupla_A in A_indexes:
            initial_conf[dupla_A[0], dupla_A[1]] = -1
      
      for dupla_B in B_indexes:
            initial_conf[dupla_B[0], dupla_B[1]] = 1
      
      return initial_conf, void_indexes

def local_happiness_segregation(matrix, row, col, satisfaction, local_value = None):
      rows, cols = len(matrix), len(matrix[0])
      if not local_value:
            local_value = matrix [row, col]
      neighbors = 0
      neighbors_equal = 0
      local_happiness = True
      
      for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                  if (0 <= i < rows and 0 <= j < cols) and (i != row or j != col):
                        if matrix[i, j] != 0:
                              neighbors +=1
                              if matrix[i, j] == local_value:
                                    neighbors_equal += 1
      if neighbors != 0:
            local_segregation = float(neighbors_equal)/float(neighbors)
      else:
            local_segregation = 1.
      if local_segregation < satisfaction:
            local_happiness = False
      
      return local_happiness, local_segregation, neighbors

def local_neighbors(matrix, row, col):
      rows, cols = len(matrix), len(matrix[0])
      neighbors_array = np.empty((0, 2), dtype=int)
      
      for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                  if (0 <= i < rows and 0 <= j < cols) and (i != row or j != col):
                        if matrix[i, j] != 0:
                              neighbors_array = np.append(neighbors_array, np.array([(i, j)]), axis=0)
      
      return neighbors_array

def cmap_creator(matrix, fig_name, A_value, B_value, directory_name):
      if not os.path.exists(directory_name):
            os.mkdir(directory_name)
      cmap = plt.get_cmap('bwr')

      # Definir los límites de color según tu rango (-1 a 1)
      vmin, vmax = A_value, B_value

      # Mostrar la matriz con el colormap y los límites
      plt.imshow(matrix, cmap=cmap, vmin=vmin, vmax=vmax, origin='lower')
      plt.savefig(directory_name+'/'+fig_name+'.png')
      plt.close()

def graphic_2_magnitudes_time(x, y1, y1_name, y2, y2_name, file_name):
      fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))  # 1 fila, 2 columnas

      # Configurar el primer gráfico
      ax1.plot(x, y1, linestyle='-', color='b', label=y1_name)
      ax1.set_xlabel('time')
      ax1.set_ylabel(y1_name)
      ax1.legend()
      ax1.grid(True)

      # Configurar el segundo gráfico
      ax2.plot(x, y2, linestyle='--', color='r', label=y2_name)
      ax2.set_xlabel('time')
      ax2.set_ylabel(y2_name)
      ax2.legend()
      ax2.grid(True)

      plt.tight_layout()  # Ajusta el espacio entre los gráficos

      plt.savefig(file_name+'.png')
      plt.close()

def new_neighborhood_magnitudes(neighbors_positions, unhappy_indexes, satisfaction, matrix):
      delta_happiness, delta_segregation = 0,0
      unhappy_indexes_list = [sub_array.tolist() for sub_array in unhappy_indexes]
      for neighbors_position in neighbors_positions:
            neighbors_position_list = neighbors_position.tolist()
            position_i = neighbors_position[0]
            position_j = neighbors_position[1]
            local_happiness, local_segregation,_ = local_happiness_segregation(matrix, position_i, position_j, satisfaction)
            if local_happiness == True:
                  delta_happiness += 1
                  if neighbors_position_list in unhappy_indexes_list:
                        # Encuentra el índice del elemento a eliminar
                        index = unhappy_indexes_list.index(neighbors_position_list)
                        del unhappy_indexes_list[index]
            else:
                  if neighbors_position_list not in unhappy_indexes_list:
                        unhappy_indexes_list.append(neighbors_position_list)
            delta_segregation += local_segregation
      unhappy_indexes = np.array(unhappy_indexes_list)
      return delta_happiness, delta_segregation, unhappy_indexes

def find_agent_to_move(unhappy_indexes, matrix, satisfaction):
      np.random.shuffle(unhappy_indexes)
      movingAgent = unhappy_indexes[0]
      unhappy_indexes = np.delete(unhappy_indexes, 0, axis=0)
      neighborsPosition = local_neighbors(matrix, movingAgent[0], movingAgent[1])
      position_i, position_j = movingAgent[0], movingAgent[1]
      local_happiness, local_segregation,_ = local_happiness_segregation(matrix, position_i, position_j, satisfaction)
      
      return unhappy_indexes, movingAgent, neighborsPosition, local_segregation

def find_new_position(void_indexes, matrix, moving_agent_value, satisfaction):
      np.random.shuffle(void_indexes)
      local_happiness = False
      aux_index = 0
      while not local_happiness:
            new_position = void_indexes[aux_index]
            position_i = new_position[0]
            position_j = new_position[1]
            local_happiness, local_segregation,_ = local_happiness_segregation(matrix, position_i, position_j, satisfaction, moving_agent_value)
            aux_index += 1
      neighborsPosition = local_neighbors(matrix, new_position[0], new_position[1])
      void_indexes = np.delete(void_indexes, aux_index-1, axis=0)
      
      return void_indexes, new_position, neighborsPosition, local_segregation

def old_neighborhood_magnitudes(neigbors, matrix, satisfaction):
      neg_delta_happiness, neg_delta_segregation = 0, 0
      for neigbor in neigbors:
            position_i, position_j = neigbor[0], neigbor[1]
            local_happiness, neg_delta_segregation,_ = local_happiness_segregation(matrix, position_i, position_j, satisfaction)
            
            if local_happiness == True:
                  neg_delta_happiness += 1
      return neg_delta_happiness, neg_delta_segregation

def GIF_creator(directory, image_files, GIF_name, frame_duration):
      if image_files:
            # We create a list of objects of PIL images
            images = [Image.open(os.path.join(directory, filename)) for filename in image_files]

            # Save the images in a GIF
            images[0].save(GIF_name+'.gif', save_all=True, append_images=images[1:], duration=frame_duration, loop=0)

system_matrix, void_indexes = rand_initial_configuration_square_lattice(lateral_size, A_individuals, B_individuals)

happiness_vec, segregation_vec = [],[]

#Absolute happiness and segregation minus the possible individuals affected
abs_happiness, abs_segregation, total_neighbors, unhappy_indexes = initial_matrix_evaluation(lateral_size, satisfaction, system_matrix)

av_neigbhors = total_neighbors/total_individuals

happiness = abs_happiness/total_individuals
segregation = abs_segregation/(av_neigbhors*total_individuals)
happiness_vec.append(happiness)
segregation_vec.append(segregation)

# Initial configuration and values
cmap_creator(system_matrix, 'initial', A_value, B_value, GIF_images_directory)

iteration = 0
while ((len(unhappy_indexes) > 0) and (iteration < maxIteration)):
      # This will compute the value lost and gained due to the agent movement
      neg_happiness, neg_segregation = 0, 0
      pos_happiness, pos_segregation = 0, 0
      
      #Finding the old position and neighbors
      unhappy_indexes, old_position, old_neighbors_positions, old_local_segregation = find_agent_to_move(unhappy_indexes, system_matrix, satisfaction)
      #We save the moving agent value
      moving_agent_value = system_matrix[old_position[0], old_position[1]]
      
      neg_happiness_old_neig, neg_segregation_old_neig = old_neighborhood_magnitudes(old_neighbors_positions, system_matrix, satisfaction)

      #We change the old position value for 0
      system_matrix[old_position[0],old_position[1]] = 0
      #We add the old position to the void positions array
      void_indexes = np.append(void_indexes, np.array([(old_position[0],old_position[1])]), axis=0)
      
      #Finding the new position and neighbors
      void_indexes, new_position, new_neighbors_positions, new_local_segregation = find_new_position(void_indexes, system_matrix, moving_agent_value, satisfaction)

      # We restore the old value for the magnitudes variation
      system_matrix[old_position[0],old_position[1]] = moving_agent_value
      neg_happiness_new_neig, neg_segregation_new_neig = old_neighborhood_magnitudes(new_neighbors_positions, system_matrix, satisfaction)
      # The old value is restored
      system_matrix[old_position[0],old_position[1]] = 0
      
      # We change the new position value for the moving agent value
      system_matrix[new_position[0],new_position[1]] = moving_agent_value

      #We change the old position value for 0
      system_matrix[old_position[0],old_position[1]] = 0
      #We compute the new contributions to the happiness and segregation
      ##Old neighbors
      pos_happiness_old_neig, pos_segregation_old_neig, unhappy_indexes = new_neighborhood_magnitudes(old_neighbors_positions, unhappy_indexes, satisfaction, system_matrix)
      ##New neighbors
      pos_happiness_new_neig, pos_segregation_new_neig, unhappy_indexes = new_neighborhood_magnitudes(new_neighbors_positions, unhappy_indexes, satisfaction, system_matrix)
      
      ##New position values will be happines = 1
      
      neg_happiness += neg_happiness_old_neig + neg_happiness_new_neig
      neg_segregation += old_local_segregation + neg_segregation_old_neig + neg_segregation_new_neig
      
      pos_happiness += 1 + pos_happiness_old_neig + pos_happiness_new_neig
      pos_segregation += new_local_segregation + pos_segregation_old_neig + pos_segregation_new_neig
      
      abs_happiness, abs_segregation = abs_happiness - neg_happiness + pos_happiness, abs_segregation - neg_segregation + pos_segregation

      happiness, segregation = abs_happiness/total_individuals, abs_segregation/(av_neigbhors*total_individuals)
      
      happiness_vec.append(happiness)
      segregation_vec.append(segregation)
      '''
      if ((iteration % frame_freq) and (createGIF)):
            cmap_creator(system_matrix, str(iteration//frame_freq), A_value, B_value, GIF_images_directory)
      '''
      iteration += 1

graphic_2_magnitudes_time([i for i in range(iteration+1)], happiness_vec, 'Happiness', segregation_vec, 'Segregation', 'magnitudes_overtime')
cmap_creator(system_matrix, str((iteration-1)//frame_freq + 1), A_value, B_value, GIF_images_directory)
"""
image_files = [str(f)+'.png' for f in range((644-1)//frame_freq + 1)]
if (createGIF):
      GIF_creator(GIF_images_directory, image_files, GIF_name, frame_duration)
"""